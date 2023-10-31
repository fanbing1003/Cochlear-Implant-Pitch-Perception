import os
import json
import pandas as pd

def FindAllFile(path):
    return(os.listdir(path))

def ReadLogFile(FileName):
    log = []
    with open(FileName) as file:
        lines = file.readlines()
        for line in lines:
            data = json.loads(line)
            if data['ws-data']['event'] == "send_event_record":
                log.append(data)
    return log

def SeperaByDevice(log):
    primary_data = []
    secondary_data = []
    for i in log:
        try:
            if i['ws-data']['data']['device_order'] == 'primary' and len(i['ws-data']['data']['adjustable_tone']) != 0:
                primary_data.append(i['ws-data']['data'])
            elif i['ws-data']['data']['device_order'] == 'secondary' and len(i['ws-data']['data']['adjustable_tone']) != 0:
                secondary_data.append(i['ws-data']['data'])
        except:
            continue
    
    return primary_data, secondary_data

def GetFinalTone(primary_data, secondary_data):
    task = ['pitch_matching_double_aided', 'pitch_matching_assess_aided', 'pitch_matching_assess_unaided', 'pitch_matching_asssess_unaided_as_control', 'pitch_matching_both_ears_desktop_speaker']
    matching_result = {}
    for i in range(5):
        target_list = []
        adj_list = []
        feedback = []
        if i <= 1:
            data = secondary_data
        else:
            data = primary_data
        task_type = task[i]
        for d in data:
            if d['task']['type'] ==  task_type:
                target_freq = d['task']['target_freqs'][0]
                if d['adjustable_tone'][-1]['event'] == 'stop_tone' or d['adjustable_tone'][-1]['event'] == 'start_tone':
                    adj_freq = d['adjustable_tone'][-1]['freq']
                elif d['adjustable_tone'][-1]['event'] == 'set_pitch':
                    adj_freq = d['adjustable_tone'][-1]['to_freq']
                target_list.append(target_freq)
                adj_list.append(adj_freq)
            
                #feedback.append(d['feedback']['txt_feedback'])   # If you need the text feedback, active this line
        matching_result[task_type] = [target_list, adj_list]
    return matching_result


def CheckCSV(data):
    tasks = ['pitch_matching_double_aided', 'pitch_matching_assess_aided', 'pitch_matching_assess_unaided', 'pitch_matching_asssess_unaided_as_control', 'pitch_matching_both_ears_desktop_speaker']
    complete = True
    #check each task, should be 5*7
    for task in tasks:
        if len(data[data['Task_Type'] == task]) != 7:
            complete = False
    #check missing value
    if data['Target_Freq'].isnull().sum() != 0 or data['Adj_Freq'].isnull().sum() != 0:
        complete = False

    if complete:
        return complete 
    else:
        return complete
    #Write Summary

def SaveAsCSV(matching_result, file_path, file_name):
    coluname = ['Task_Type', "Target_Freq", "Adj_Freq"]
    df = pd.DataFrame(columns=coluname)
    for i in matching_result.keys():
        for j in range(len(matching_result[i][0])):                                                                  
            df.loc[len(df)] = [i, matching_result[i][0][j], matching_result[i][1][j]]
            #df.loc[len(df)] = [i, matching_result[i][0][j], matching_result[i][1][j], matching_result[i][2][j]]
    
    if CheckCSV(df):
        df.to_csv(file_path + '/complete/' + file_name + 'csv', index=False)
    else:
        df.to_csv(file_path + '/incomplete/' + file_name + 'csv', index=False)


if __name__ == '__main__':
    log_path = 'Your log file folder'
    save_path = 'Folder to save the extracted data'
    logs = FindAllFile(log_path)
    # Extraction
    
    for log in logs:
        try:
            l = ReadLogFile(log_path+'/'+log)
           
            Primary_data, Secondary_data = SeperaByDevice(l)
            
            match_dict = GetFinalTone(Primary_data, Secondary_data)
            
            SaveAsCSV(match_dict, save_path, log[:-3])
        except:
            print(log)
        


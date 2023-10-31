library(nortest)
library("car")
setwd('./TaskbyTask')


# Task1---------------------------------------------------------------------------------------
Task1 = read.csv('pitch_matching_double_aided.csv')
Task1$Tar_octave = log(Task1$Tar/27.5, 2)
Task1$diff_freq = Task1$Adj - Task1$Tar
Task1$diff_octave = log(Task1$Adj/Task1$Tar, 2)
Task1$order = 1:392

model = lm(diff_freq ~ Tar_octave + order , data = Task1)
summary(model)
plot(Task1$Tar, Task1$diff_octave)
plot(model$residuals)
ad.test(model$residuals)
qqPlot(model$residuals)

# Task2---------------------------------------------------------------------------------------
Task2 = read.csv('pitch_matching_assess_aided.csv')
Task2$Tar_octave = log(Task2$Tar/27.5, 2)
Task2$diff_freq = Task2$Adj - Task2$Tar
Task2$diff_octave = log(Task2$Adj/Task2$Tar, 2)
Task2$order = 1:392

model = lm(diff_freq ~ Tar_octave + order -1, data = Task2)
summary(model)
plot(Task2$Tar, Task2$diff_octave)
plot(model$residuals)
ad.test(model$residuals)
qqPlot(model$residuals)

# Task3---------------------------------------------------------------------------------------
Task3 = read.csv('pitch_matching_assess_unaided.csv')
Task3$Tar_octave = log(Task3$Tar/27.5, 2)
Task3$diff_freq = Task3$Adj - Task3$Tar
Task3$diff_octave = log(Task3$Adj/Task3$Tar, 2)
Task3$order = 1:392


model = lm(diff_freq ~ Tar_octave + order , data = Task3)
summary(model)
plot(Task3$Tar, Task3$diff_octave)
plot(model$residuals)
ad.test(model$residuals)
qqPlot(model$residuals)

# Task4---------------------------------------------------------------------------------------
# Can't find specific trends
Task4 = read.csv('pitch_matching_assess_unaided_as_control.csv')
Task4$Tar_octave = log(Task4$Tar/27.5, 2)
Task4$diff_freq = Task4$Adj - Task4$Tar
Task4$diff_octave = log(Task4$Adj/Task4$Tar, 2)
Task4$order = 1:392

ad.test(Task4$diff_freq)
ks.test(Task4$diff_freq, 'pnorm')
plot(density(Task4$diff_freq))
qqPlot(Task4$diff_freq)


library(ggplot2)
ggplot(data = Task4, aes(x = order, y = diff_freq)) + 
  geom_smooth()+
  geom_point()

model = lm(diff_freq ~ Tar_octave + order - 1, data = Task4)
summary(model)
plot(Task4$Tar, Task4$diff_octave)
plot(model$residuals)
ad.test(model$residuals)
qqPlot(model$residuals)


# Task5---------------------------------------------------------------------------------------
Task5 = read.csv('pitch_matching_both_ears_desktop_speaker.csv')
Task5$Tar_octave = log(Task5$Tar/27.5, 2)
Task5$diff_freq = Task5$Adj - Task5$Tar
Task5$diff_octave = log(Task5$Adj/Task5$Tar, 2)
Task5$order = 1:392

model = lm(diff_freq ~ Tar_octave + order - 1, data = Task5)
summary(model)
plot(Task5$Tar, Task5$diff_octave)
plot(model$residuals)
ad.test(model$residuals)
qqPlot(model$residuals)
#Consider the perfect matching, difference only depends on  number of trail and the target freq. 
# i.e. no constant terms. That's why we remove constant terms.
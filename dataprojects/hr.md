# People Analytics

In this project, I took on the role of "People Data Analyst" for a fictional HR department. My job is to explore issues including accusations of ageism.

## The Dataset

The dataset was created by data scientists at IBM, and can be found [here](https://hoswaymolina.github.io/dataprojects/iron.html).

## Analysis

The first step was simply to import the data:

```r
hrdata <- read.csv("HR-Employee-Attrition.csv")
```

After doing this, the first thing I did was check if any of the demographic characteristics had any correlations. I used the "cor" method on the most relevant columns:

```r
cor(hrdata[, c("Age", "DailyRate", "DistanceFromHome", "Education", "HourlyRate", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "TotalWorkingYears", "TrainingTimesLastYear")])
```

<img alt="image" src="https://github.com/user-attachments/assets/869a245c-f71c-493b-8244-1ef5f104e65e" />

Shown above is a subset of the correlation matrix. Among the strongest correlations are those between income, age, and years worked/trained, which makes sense - the more experience someone has, the more money they should make. For example, monthly income and total working years have a correlation value of .773; age and monthly income are almost at .500.

It made sense to visualize these relationships with scatter plots, and just like in Python, we have a simple built-in command to get some pair plots:

```r
pairs(~MonthlyIncome + Age + TotalWorkingYears + Education, data = hrdata, main = "Scatterplot Matrix")
```

<img alt="image" src="https://github.com/user-attachments/assets/2b998eeb-da7a-4c9e-9996-5bac8520b6d1" />

As we expect, income/working years and income/age have rather strong correlations. However, I noticed something interesting - the age and working years variables have a very smooth upper/lower range so that the plot looks like it's inside of a right triangle. It's like there's an upper or lower bound defined by a linear equation. In this case, for a given age, there is a maximum possible number of working years. Upon further inspection, I realized this makes sense, since generally speaking, one cannot begin employment until they are a certain age. So, the line defining the maximum possible years worked represents is in fact a hard and fast bound.

It was then time to answer the accusations of ageism. An employee has sued the company, saying that layoffs were age-based. I checked this by observing the age distributions for those who were let go and those who remained. I did this with a boxplot

```r
boxplot(Age~Attrition, data=hrdata, main= "Who Got Fired", xlab="Attrition", ylab="Age")
```


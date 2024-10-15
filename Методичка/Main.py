import csv
import json
import pandas as pd
from datetime import datetime, timedelta
from termcolor import colored, cprint

df = pd.read_csv('Методичка.csv')

df['Дата найма'] = pd.to_datetime(df['Дата найма'], format='%d.%m.%Y')

# №1 Начальство решило выплачивать премии ко дню программиста в сентябре (13
# сентября – день программиста). Премия будет составлять 3% от оклада каждому
# программисту. Реализуйте функцию, которая будет рассчитывать премию.
def bonus_for_programmers(df):
    bonus_percentage =0.03
    programmers = df[df['Должность'].str.contains(' программист', case=False)]
    programmers['Премия'] = programmers['Оклад']*bonus_percentage
    return programmers[['ФИО','Должность', 'Премия']]


programmer_bonus = bonus_for_programmers(df)
print(colored('\n№1', 'light_red'))
print(colored( "Премии ко дню программиста:", 'light_red'))
print(programmer_bonus)

# №2 Начальство решило выплачивать премии к 8 марта всем сотрудницам, а к 23
# февраля сотрудникам, равные 2000 Реализуйте функцию, которая будет
# рассчитывать премию.
def gender_bonus(df):
    df['Премия на 23 февраля'] = 0
    df['Премия на 8 марта'] = 0

    male = df[df['ФИО'].str.contains('вич')]
    df.loc[male.index, 'Премия на 23 февраля'] = 2000
    
    fem = df[df['ФИО'].str.contains('вна')]
    df.loc[fem.index, 'Премия на 8 марта']= 2000
    return df[['ФИО', 'Должность', 'Оклад', 'Премия на 23 февраля', 'Премия на 8 марта']]

gen_bon=gender_bonus(df)
print(colored("\n№2",'light_red'))
print(colored("Премии на 8 марта и 23 февраля:", 'light_red'))
print(gen_bon)

# №3 Было решено провести индексацию зарплат сотрудников. Сотрудникам, которые
# отработали в компании более 10 лет, индексация будет равна 7% оклада,
# остальным – 5%.
def indexation_salary(df):
    current_date = datetime.now()
    df['Период работы'] = (current_date - df['Дата найма']).dt.days/365
    df['Индексация']=0
    
    # Индексация для сотрудников с опытом более 10 лет
    df.loc[df['Период работы'] > 10, 'Индексация'] = df['Оклад'] * 0.07
    df.loc[df['Период работы'] <= 10, 'Индексация'] = df['Оклад'] * 0.05
    
    return df[['ФИО', 'Должность', 'Дата найма','Индексация']]

index_sal = indexation_salary(df)
print(colored("\n№3",'light_red'))
print(colored("Индексация зарплат:", 'light_red'))
print(index_sal)

# №4 Необходимо составить график отпусков сотрудников. Для этого необходимо в
# отдельный список занести тех сотрудников, которые отработали в компании более
# 6 месяцев. Реализовать функцию.
def vacation_for_employees(df):
    current_date = datetime.now()
    df['Период работы в днях']= (current_date - df['Дата найма']).dt.days
    employees_with_six_months = df[df['Период работы в днях'] > 182.5]
    return employees_with_six_months[['ФИО', 'Должность', 'Период работы в днях']]

vacation = vacation_for_employees(df)
print(colored("\n№4",'light_red'))
print(colored("Сотрудники, отработавшие больше 6 месяцев:", 'light_red'))
print(vacation)


# №5 Реализуйте функции записи в csv и json.
def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(colored(f"Данные сохранены в файл {filename}", 'green'))

dfj = df.to_json()
def save_to_json(df, filename):
    with open(filename, 'w') as json_file:
        json.dump(dfj, json_file)
    print(colored(f"Данные сохранены в файл {filename}", 'green'))


print(colored("\n№5",'light_red'))
save_to_csv(programmer_bonus, 'programmer_bonus.csv')
save_to_json(programmer_bonus, 'programmer_bonus.json')
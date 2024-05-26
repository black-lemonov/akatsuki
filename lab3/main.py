import tkinter
import time
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Combobox, Notebook
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from Rosenbrock_function import make_data_lab_3
from genetic_algorithm import GeneticAlgorithm
from functions import *

def main():
    window = Tk()

    window.geometry("1000x800")

    window.title("Генетический алгоритм")

    fig = plt.figure(figsize=(14, 14))
    fig.add_subplot(projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)


    tab_control = Notebook(window)

    # ЛР №3
    def draw_lab_3():
        fig.clf()

        x, y, z = make_data_lab_3()

        pop_number = int(txt_1_tab_3.get())
        iter_number = int(txt_2_tab_3.get())
        survive = float(txt_3_tab_3.get())
        mutation = float(txt_4_tab_3.get())
        delay = txt_5_tab_3.get()

        if combo_tab_3.get() == "Min":
            min_max = True
        else:
            min_max = False

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5)
        canvas.draw()

        genetic = GeneticAlgorithm(rosenbrock_2, iter_number, min_max, mutation, survive, pop_number)
        genetic.generate_start_population(5, 5)

        for j in range(pop_number):
            ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1,
                       marker="s")
        if min_max:
            gen_stat = list(genetic.statistic()[1])
        else:
            gen_stat = list(genetic.statistic()[0])

        ax.scatter(gen_stat[1][0], gen_stat[1][1], gen_stat[1][2], c="red")
        canvas.draw()
        window.update()

        #Строки 89-92 удаляют точк(у/и)
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5)
        canvas.draw()

        for i in range(50):
            for j in range(pop_number):
                ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1,
                           marker="s")

            genetic.select()
            genetic.mutation(i)

            if min_max:
                gen_stat = list(genetic.statistic()[1])
            else:
                gen_stat = list(genetic.statistic()[0])

            ax.scatter(gen_stat[1][0], gen_stat[1][1], gen_stat[1][2], c="red")

            txt_tab_3.insert(INSERT,
                             f"{i}) ({round(gen_stat[1][0], 4)}) ({round(gen_stat[1][1], 4)}) = "
                             f" ({round(gen_stat[1][2], 4)})\n")

            canvas.draw()
            window.update()
            time.sleep(float(delay))

            fig.clf()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5)
            canvas.draw()

        for j in range(pop_number):
            ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1,
                       marker="s")
        if min_max:
            gen_stat = list(genetic.statistic()[1])
        else:
            gen_stat = list(genetic.statistic()[0])

        ax.scatter(gen_stat[1][0], gen_stat[1][1], gen_stat[1][2], c="red")

        canvas.draw()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        window.update()

        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_3():
        txt_tab_3.delete(1.0, END)

    tab_3 = Frame(tab_control)
    tab_control.add(tab_3, text="LR3")

    main_f_tab_3 = LabelFrame(tab_3, text="Параметры")
    left_f_tab_3 = Frame(main_f_tab_3)
    right_f_tab_3 = Frame(main_f_tab_3)
    txt_f_tab_3 = LabelFrame(tab_3, text="Выполнение и результаты")

    lbl_1_tab_3 = Label(left_f_tab_3, text="Размер популяции")
    lbl_2_tab_3 = Label(left_f_tab_3, text="Количество итераций")
    lbl_3_tab_3 = Label(left_f_tab_3, text="Выживаемость")
    lbl_7_tab_3 = Label(left_f_tab_3, text="Шанс мутации")
    #lbl_4_tab_3 = Label(left_f_tab_3, text="Выбор точки поиска")
    lbl_5_tab_3 = Label(left_f_tab_3, text="Задержка в секундах")
    lbl_6_tab_3 = Label(tab_3, text="Функция Розенброка")

    txt_1_tab_3 = Entry(right_f_tab_3)
    txt_1_tab_3.insert(0,"20")
    txt_2_tab_3 = Entry(right_f_tab_3)
    txt_2_tab_3.insert(0,"50")
    txt_3_tab_3 = Entry(right_f_tab_3)
    txt_3_tab_3.insert(0,"0.8")
    txt_4_tab_3 = Entry(right_f_tab_3)
    txt_4_tab_3.insert(0,"0.8")
    txt_5_tab_3 = Entry(right_f_tab_3)
    txt_5_tab_3.insert(0,"0.01")

    combo_tab_3 = Combobox(right_f_tab_3)
    combo_tab_3['values'] = ("Min", "Max")
    combo_tab_3.set("Min")

    txt_tab_3 = scrolledtext.ScrolledText(txt_f_tab_3)
    btn_del_tab_3 = Button(tab_3, text="Очистить", foreground="black", background="red", command=delete_lab_3)
    btn_tab_3 = Button(tab_3, text="Выполнить", foreground="black", background="#08fc30", command=draw_lab_3)

    lbl_6_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    main_f_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_3.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_3.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_1_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_2_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_3_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_7_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_5_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    #lbl_4_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_3_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_4_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)  # задержка в секундах
    txt_5_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)  # шанс мутации
    #combo_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_3.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_3.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_3.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_3.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    tab_control.pack(side=RIGHT, fill=BOTH, expand=True)
    window.mainloop()

if __name__ == '__main__':
    main()
import tkinter
import time
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Notebook
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pso import PSO
from functions import *

def main():
    window = Tk()

    window.geometry("1000x800")

    window.title("Алгоритм роя частиц")

    fig = plt.figure(figsize=(14, 14))
    fig.add_subplot(projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)


    tab_control = Notebook(window)

    # Лаба 4
    def draw_lab_4():
        fig.clf()

        #x, y, z = make_data_lab_3()
        px = 5.0
        py = 5.0
        x, y, z = make_data_rastrigin(px, py)

        iterations = int(txt_1_tab_4.get())
        particles_number = int(txt_2_tab_4.get())
        fi_p = float(txt_4_tab_4.get())
        fi_g = float(txt_5_tab_4.get())
        delay = txt_6_tab_4.get()

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5)
        canvas.draw()

        psa_obj = PSO(rastrigin_2, particles_number, px, py, fi_p, fi_g)

        for particle in psa_obj.particles:
            ax.scatter(particle[0], particle[1], particle[2], c="black", s=1, marker="s")

        ax.scatter(psa_obj.generation_best[0], psa_obj.generation_best[1], psa_obj.generation_best[2], c="red")
        canvas.draw()
        window.update()

        # Эти 4 строки ниже отвечают за удаление точки
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5)
        canvas.draw()

        for i in range(iterations):
            
            # обновляет скорость и позицию каждой частицы, 
            # а также находит новую лучшую частицу в поколении
            
            for j in range(particles_number):

                if psa_obj.nostalgia[j][2] < psa_obj.particles[j][2]:
                    point_best = psa_obj.nostalgia[j]
                else:
                    psa_obj.nostalgia[j] = psa_obj.particles[j]
                    point_best = psa_obj.particles[j]

                psa_obj.velocity[j] = psa_obj.update_velocity(psa_obj.velocity[j], psa_obj.particles[j], point_best)
                psa_obj.particles[j] = psa_obj.update_position(psa_obj.velocity[j], psa_obj.particles[j])

            psa_obj.generation_best = min(psa_obj.particles, key=lambda x: x[2])
            
            for particle in psa_obj.particles:
                ax.scatter(particle[0], particle[1], particle[2], c="black", s=1, marker="s")

            ax.scatter(psa_obj.generation_best[0], psa_obj.generation_best[1], psa_obj.generation_best[2], c="red")

            txt_tab_4.insert(INSERT,
                             f"{i + 1}) ({round(psa_obj.generation_best[0], 8)})"
                             f" ({round(psa_obj.generation_best[1], 8)}) = "
                             f" ({round(psa_obj.generation_best[2], 8)})\n")

            canvas.draw()
            window.update()
            time.sleep(float(delay))

            fig.clf()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5)
            canvas.draw()

        for particle in psa_obj.particles:
            ax.scatter(particle[0], particle[1], particle[2], c="black", s=1, marker="s")

        ax.scatter(psa_obj.generation_best[0], psa_obj.generation_best[1], psa_obj.generation_best[2], c="red")

        canvas.draw()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        window.update()

        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_4():
        txt_tab_4.delete(1.0, END)

    tab_4 = Frame(tab_control)
    tab_control.add(tab_4, text="ЛР4")

    main_f_tab_4 = LabelFrame(tab_4, text="Параметры")
    left_f_tab_4 = Frame(main_f_tab_4)
    right_f_tab_4 = Frame(main_f_tab_4)
    txt_f_tab_4 = LabelFrame(tab_4, text="Выполнение и результаты")

    lbl_1_tab_4 = Label(left_f_tab_4, text="Количество итераций")
    lbl_2_tab_4 = Label(left_f_tab_4, text="Количество частиц")
    lbl_4_tab_4 = Label(left_f_tab_4, text="Коэффициент g")
    lbl_5_tab_4 = Label(left_f_tab_4, text="Задержка в секундах")
    lbl_6_tab_4 = Label(tab_4, text="Функция Растригина")
    lbl_7_tab_4 = Label(left_f_tab_4, text="Коэффициент p")

    txt_1_tab_4 = Entry(right_f_tab_4)
    txt_1_tab_4.insert(0, "100")
    txt_2_tab_4 = Entry(right_f_tab_4)
    txt_2_tab_4.insert(0, "50")
    txt_4_tab_4 = Entry(right_f_tab_4)
    txt_4_tab_4.insert(0, "5")
    txt_5_tab_4 = Entry(right_f_tab_4)
    txt_5_tab_4.insert(0, "5")
    txt_6_tab_4 = Entry(right_f_tab_4)
    txt_6_tab_4.insert(0, "0.01")

    txt_tab_4 = scrolledtext.ScrolledText(txt_f_tab_4)
    btn_del_tab_4 = Button(tab_4, text="Очистить", background="red",command=delete_lab_4)
    btn_tab_4 = Button(tab_4, text="Выполнить", foreground="black", background="#08fc30", command=draw_lab_4)

    lbl_6_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    main_f_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_4.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_4.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_1_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_2_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_7_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_4_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_5_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_4_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_5_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_6_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_4.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_4.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_4.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_4.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    tab_control.pack(side=RIGHT, fill=BOTH, expand=True)
    window.mainloop()

if __name__ == '__main__':
    main()
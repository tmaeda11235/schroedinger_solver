from schrpy import Note

note = Note(-10, 10, 0.1, 0, 5, 0.1)
note.solve_schroedinger_equation()
note.easy_plot2d(title="test", save=True)

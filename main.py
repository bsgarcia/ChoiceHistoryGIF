import numpy as np
import pandas as pd

from moviepy.editor import ImageSequenceClip
from exp.exp import ExperimentGUI


def main():

    filename = 'block'

    # load data
    data = pd.read_csv(f'data/{filename}.csv')
    #mask1 = np.array((data['sym_cor'] == 1))
    #mask2 = np.array((data['sym_incor'] == 1))

    #data = data[mask1 + mask2]

    #mask3 = np.array((data['sym_cor'] == 7))
    #mask4 = np.array((data['sym_incor'] == 7))

    #data['sym_cor'][mask1] = 7
    #data['sym_incor'][mask2] = 7
    #data['sym_cor'][mask3] = 1
    #data['sym_incor'][mask4] = 1

    trial_obj = []
    for t, _ in data.iterrows():
        trial_obj.append({
            't': data['trial.choiceType'][t],
            'outcome1': data['outcome_cor'][t],
            'outcome2': data['outcome_incor'][t],
            'sym1': str(data['sym_cor'][t]),
            'sym2': str(data['sym_incor'][t]),
            'choice': data['resp.cor'][t] == 0,
            'inverted': data['position_cor'][t]
        })

    # ------------------------------------------------------------------ # 
    # Start experiment                                                   #
    # ------------------------------------------------------------------ # 
    exp = ExperimentGUI(name="RetrospectTheory")
    exp.init()
    exp.run(trial_obj)

    frames = [np.array(frame) for frame in exp.win.movieFrames]
    clip = ImageSequenceClip(frames, fps=2)
    clip.write_videofile(f'{filename}.mp4')
    clip.write_gif(f'{filename}.gif')


if __name__ == "__main__":
    main()

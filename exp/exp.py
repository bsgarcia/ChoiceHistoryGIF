import os
import numpy as np
import codecs
import csv
import psychopy as psy
from psychopy import data, core, event, gui, visual


class AbstractGUI:
    """

    Abstract GUI Component

    """

    def __init__(self, *args, **kwargs):
        self.win = None
        self.exp_info = None
        self.info_dlg = None
        self.name = None
        self.datafile = None
        self.stim = None

        self.name = kwargs.get('name')
        self.img_list = kwargs.get('img_list')

    def init_experiment_window(self):
        self.win = psy.visual.Window(
            size=(1300, 740),
            fullscr=False,
            screen=0,
            allowGUI=False,
            allowStencil=False,
            monitor='testMonitor',
            color='white',
            colorSpace='rgb',
            blendMode='avg',
            winType='pyglet',
            autoDraw=False
        )

    @staticmethod
    def create_text_stimulus(win, text, height, color, wrapwidth=None):

        text = psy.visual.TextStim(
            win=win,
            ori=0,
            text=text,
            font='Arial',
            height=height,
            color=color,
            colorSpace='rgb',
            alignHoriz='center',
            alignVert='center',
            wrapWidth=wrapwidth
        )
        return text

    @staticmethod
    def create_text_box_stimulus(win, pos, boxcolor='white',
                                 outline='black', linewidth=1):
        rect = psy.visual.Rect(
            win=win,
            width=.40,
            height=.7,
            #fillColor=boxcolor,
            lineColor=outline,
            lineWidth=linewidth,
            pos=pos,
        )
        return rect

    @staticmethod
    def present_stimulus(obj, pos=None, size=None):
        if size:
            obj.setSize(size)
        if pos:
            obj.setPos(pos)

        obj.draw()

    @staticmethod
    def make_dir(dirname):
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    @staticmethod
    def get_files(path='./resources'):
        return [file for i, j, file in os.walk(path)][0]

    @staticmethod
    def load_files(win, files, path='resources/'):
        stim = {}
        for filename in sorted(files):

            ext = filename[-3:]
            name = filename[:-4]

            if ext in ('bmp', 'jpg', 'png', 'gif'):
                stim[name] = psy.visual.ImageStim(
                    win, image=f'{path}{filename}',# size=(.7, .8)#color='white'
                )

            elif ext == 'txt':

                with codecs.open(f'{path}{filename}', 'r') as f:
                    stim[name] = psy.visual.TextStim(
                        win,
                        text=f.read(),
                        wrapWidth=1.2,
                        alignHoriz='center',
                        alignVert='center',
                        height=0.20
                    )
        return stim

    def init(self):

        # Show exp window
        self.init_experiment_window()

        # Load files
        path = 'resources/symbols/'
        names = self.get_files(path=path)
        self.stim = self.load_files(win=self.win, files=names, path=path)


class ExperimentGUI(AbstractGUI):
    """

    GUI component

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #  experiment parameters
        self.pos_left = [-0.4, 0]
        self.pos_right = [0.4, 0]
        self.pos_up = [0, 0.3]
        self.pos_down = [0, -0.3]

    def display_selection(self, left_or_right):
        pos = [self.pos_left, self.pos_right][left_or_right][:]
        self.present_stimulus(self.create_text_box_stimulus(self.win, pos=pos, linewidth=7))

        pos[1] -= .83
        self.present_stimulus(self.stim['arrow'], pos=pos, size=(.15, .25))

    def display_fixation(self):
        self.present_stimulus(self.stim['cross'])

    def display_welcome(self):
        self.stim['welcome'].setHeight(0.06)
        self.present_stimulus(self.stim['welcome'])

    def display_end(self):
        self.present_stimulus(self.stim['end'])

    def display_counterfactual_outcome(self, outcomes, choice, inverted, color='black'):
        pos, text = [self.pos_left, self.pos_right], [None, None]

        # set order
        cf_out = outcomes[not choice]
        out = outcomes[choice]
        text[choice] = \
            f'+{out}' if out > 0 else f'{out}'
        text[not choice] = \
            f'+{cf_out}' if cf_out > 0 else f'{cf_out}'
        order = [[0, 1], [1, 0]][inverted]
        text = np.array(text)[order]

        # Display
        for t, p in zip(text, pos):
            self.present_stimulus(
                self.create_text_stimulus(win=self.win, text=t, color=color, height=0.4), pos=(p[0], p[1]-.5)
            )

    def display_outcome(self, outcome, left_or_right, color='red'):
        pos = [self.pos_left, self.pos_right][left_or_right][:]
        text = f'+{outcome}' if outcome > 0 else f'{outcome}'
        self.present_stimulus(
            self.create_text_stimulus(win=self.win, text=text, color=color, height=0.13),
            pos=pos
        )

    def display_pair(self, left, right):
        self.present_stimulus(self.stim[left], pos=self.pos_left, size=[0.40, .7])
        self.present_stimulus(self.stim[right], pos=self.pos_right, size=[0.40, .7])

    def display_time(self, t):
        self.present_stimulus(self.create_text_stimulus(
                self.win, text='t = ' + str(t), color='black', height=0.24), pos=(0.8, 0.85)
        )

    def run(self, trial_obj):

        self.win.flip()

        for trial in trial_obj:

            t = trial['t']
            inverted = trial['inverted']
            choice = trial['choice']
            sym1 = trial['sym1']
            sym2 = trial['sym2']
            outcome1 = trial['outcome1']
            outcome2 = trial['outcome2']

            symbols = [[sym1, sym2],
                       [sym2, sym1]][inverted]

            self.display_pair(*symbols)
            self.display_time(t)

            self.win.flip()
            self.win.getMovieFrame()

            self.display_time(t)
            self.display_pair(*symbols)

            left_right = [choice, not choice][inverted]
            self.display_selection(left_right)

            self.win.flip()
            self.win.getMovieFrame()

            self.display_counterfactual_outcome(
                outcomes=[outcome1, outcome2],
                choice=choice,
                inverted=inverted
            )
            self.display_pair(*symbols)

            self.display_time(t)
            self.display_selection(left_or_right=left_right)
            self.win.flip()
            self.win.getMovieFrame()


if __name__ == '__main__':
    exit('Please run the main.py script')

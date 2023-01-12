from playsound import playsound
from glob import glob
import os
import random
import time
from datetime import datetime
import csv


class Tone(object):
    def __init__(self, name: str):
        super(Tone, self).__init__()
        self.name = name
        self.correct = 0
        self.fails = 0
        self.samples = []
        self.soundName = ""
        self.repeated = 0

    def GetSoundName(self):
        return self.soundName

    def GetRepetitions(self):
        return self.repeated

    def GetCorrect(self):
        return self.correct

    def GetFails(self):
        return self.fails

    def Correct(self):
        self.correct += 1

    def Failed(self):
        self.fails += 1

    def GetName(self):
        return self.name

    def SetSamples(self, path):
        self.samples.append(path)

    def SetSamplesList(self, pathList):
        self.samples = pathList

    def Repeat(self):
        self.repeated += 1
        if self.soundName:
            self.Play()

    def Play(self):
        playsound(self.soundName, block=False)

    def PlayRandom(self):
        self.soundName = random.choice(self.samples)
        playsound(self.soundName, block=True)
        return self.soundName


class PitchTrainer(object):
    def __init__(self):
        super(PitchTrainer, self).__init__()
        self.tonesPaths = []
        self.folders = []
        self.lastTone = Tone("A")
        self.lastToneRepeated = 0
        self.notesPlayed = 0
        self.dataHeader = []
        self.tones = []
        self.statistics = []
        self.toneClassList = []
        mydate = datetime.now()
        self.time = datetime.strftime(mydate, '%Y, %m, %d, %H, %M, %S')

    def LoadNotes(self):
        for folder in glob('*/'):
            self.folders.append(folder)
        # print(self.folders)
        for folder in self.folders:
            tonePath = []
            for file in glob(folder+'*'):
                # print(file)
                tonePath.append(file)
            self.tonesPaths.append(tonePath)
        # print(self.noteArray)
        self.GetAllToneNames()
        self.CreateTones(self.tones, self.tonesPaths)

    def GetAllToneNames(self) -> list:
        for item in self.tonesPaths:
            self.tones.append(item[0][0])
        # print(self.tones)
        return self.tones

    def CreateTones(self, toneList, tonesPaths):
        for item in toneList:
            self.toneClassList.append(Tone(item))
        for i, tone in enumerate(self.toneClassList):
            tone.SetSamplesList(tonesPaths[i])

    def PlayRandomNote(self):
        # select random tone
        self.lastTone = (random.choice(self.toneClassList))
        self.lastTone.PlayRandom()
        self.notesPlayed += 1

    def PlayLastTone(self):
        self.lastTone.Repeat()

    def GetLastTone(self):
        return self.lastTone

    def CheckCorrect(self, guessedTone):
        currentTone = self.lastTone
        if(guessedTone == currentTone.GetName()):
            print("Correct (: Your guess: {} Tone was: {}.".format(
                guessedTone, currentTone.GetName()))
            currentTone.Correct()
        else:
            currentTone.Failed()
            print("Failed  ): Your guess: {} Tone was: {}.".format(
                guessedTone, currentTone.GetName()))
        self.PlayRandomNote()

    def PrintStats(self):
        for item in self.toneClassList:
            print("{} ok: {} failed: {} repeated: {}".format(
                item.GetName(), item.GetCorrect(), item.GetFails(), item.GetRepetitions()))

    def WriteStats(self):
        fields = self.CreateHeader()
        amountOfSkips = len(self.time.split(','))
        idx = 0
        idxTone = 0
        for i, _ in enumerate(fields):
            if i < amountOfSkips:
                fields[i] = self.time.split(',')[i]
            if i == amountOfSkips:
                fields[i] = self.notesPlayed
            if i > amountOfSkips:
                if idx == 0:
                    fields[i] = self.toneClassList[idxTone].GetCorrect()
                if idx == 1:
                    fields[i] = self.toneClassList[idxTone].GetFails()
                if idx == 2:
                    fields[i] = self.toneClassList[idxTone].GetRepetitions()
                    idxTone += 1
                if idx == 2:
                    idx = 0
                else:
                    idx += 1
        print(fields)
        with open(r'data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    def CreateHeader(self):
        fields = ['Year, Month, Day, Hour, Minute, Second']
        fields = ''.join(fields).split(', ')
        fields.append("Number of tones")
        for item in self.toneClassList:
            toneName = item.GetName()
            fields.append(toneName+"_OK")
            fields.append(toneName+"_FAIL")
            fields.append(toneName+"_REPEATED")
        return fields

    def WriteHeader(self):
        fields = self.CreateHeader()
        print(fields)
        with open(r'data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    def PrintCommands(self):
        commands = """
    Commands:
    n - next tone
    r - repeat tone
    g - get tone name
    h - this help
    s - save data
    p - print data
    q - quit
    """
        commands += ','.join(self.tones)
        commands += " - guess the note\n"
        print(commands)


def main():
    print("\n|Pitch| trainer by Daniel")

    trainer0 = PitchTrainer()
    trainer0.LoadNotes()
    # trainer0.WriteHeader()
    x = 'h'
    while(1):
        match x:
            case 'h':
                trainer0.PrintCommands()
            case 'n':
                trainer0.PlayRandomNote()
            case 'g':
                print(trainer0.GetLastTone().GetSoundName())
            case 'p':
                trainer0.PrintStats()
            case 's':
                trainer0.WriteStats()
            case 'r':
                if(trainer0.GetLastTone()):
                    trainer0.PlayLastTone()
            case 'q':
                y = input("want to save data? y/n ")
                if y == "y":
                    trainer0.WriteStats()
                print("nashledanou ^^")
                break
            case _:
                if x in trainer0.tones:
                    trainer0.CheckCorrect(x)
        x = input("Select:")


if __name__ == "__main__":
    main()

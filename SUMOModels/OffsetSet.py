class OffsetSet:
    def __init__(self, offsetList, controlParaList):
        self.ol = offsetList
        self.cpl = controlParaList

    def genHead(self, jID, offset, f):
        print('    <tlLogic id="j_{}" type="static" programID="1" offset="{}">'.format(jID, offset), file=f)

    def genPhases(self, cp, f):
        print('        <phase duration="%d" state="GGgGrrGrrGrr"/>' % cp[0], file=f)
        print('        <phase duration="2" state="GyyGrrGrrGrr"/>', file=f)
        print('        <phase duration="1" state="GrrGrrGrrGrr"/>', file=f)
        print('        <phase duration="%d" state="GrrGGgGrrGrr"/>' % cp[1], file=f)
        print('        <phase duration="2" state="GrrGyyGrrGrr"/>', file=f)
        print('        <phase duration="1" state="GrrGrrGrrGrr"/>', file=f)
        print('        <phase duration="%d" state="GrrGrrGGgGrr"/>' % cp[2], file=f)
        print('        <phase duration="2" state="GrrGrrGyyGrr"/>', file=f)
        print('        <phase duration="1" state="GrrGrrGrrGrr"/>', file=f)
        print('        <phase duration="%d" state="GrrGrrGrrGGg"/>' % cp[3], file=f)
        print('        <phase duration="2" state="GrrGrrGrrGyy"/>', file=f)
        print('        <phase duration="1" state="GrrGrrGrrGrr"/>', file=f)

    def genAddFile(self):
        with open('GridNetwork_offset.add.xml', 'w') as f:
            print('<additional>', file=f)
            for i in range(9):
                self.genHead(i + 1, self.ol[i], f)
                self.genPhases(self.cpl[i], f)
                print('    </tlLogic>', file=f)
            print('</additional>', file=f)


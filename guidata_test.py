from guidata.dataset.datatypes import DataSet, BeginGroup, EndGroup, GetAttrProp, FuncProp
from guidata.dataset.dataitems import (FloatItem, IntItem, BoolItem, ChoiceItem,
                             MultipleChoiceItem, ImageChoiceItem, FilesOpenItem,
                             StringItem, TextItem, ColorItem, FileSaveItem,
                             FileOpenItem, DirectoryItem, FloatArrayItem,
                             DateItem, DateTimeItem)

legendchoices = ((None, 'None'),
                    ('TR', 'Top Right'),
                    ('BR', 'Bottom Right'),
                    ('BL', 'Bottom Left'),
                    ('TL', 'Top Left'))

choices = (('A', 'Choice #1: A'), ('B', 'Choice #2: B'), ('C', 'Choice #3: C'))

class Test(DataSet):
    fname = FileOpenItem("Open file", ("log", "txt"), 'sample_data.log')

    _prop = GetAttrProp("choice")
    choice = ChoiceItem('Choice', choices).set_prop("display", store=_prop)
    _bg = BeginGroup("sub group 1").set_prop("display",
                                  active=FuncProp(_prop, lambda x: x=='B'))

    color = ColorItem("Color")
    choice2 = ChoiceItem("Single choice 1",
                        [(16, "first choice"), (32, "second choice"),
                         (64, "third choice")])
    mchoice2 = ImageChoiceItem("Single choice 2",
                               [("rect", "first choice", "gif.png" ),
                                ("ell", "second choice", "txt.png" ),
                                ("qcq", "third choice", "file.png" )]
                               )
    _eg = EndGroup("sub group 1")

    x1 = FloatItem('x1')
    x2 = FloatItem('x2').set_prop("display",
                                  active=FuncProp(_prop, lambda x: x=='B'))
    x3 = FloatItem('x3').set_prop("display",
                                  active=FuncProp(_prop, lambda x: x=='C'))

if __name__ == '__main__':
    # Create QApplication
    import guidata
    _app = guidata.qapplication()

    test = Test()
    test.edit()

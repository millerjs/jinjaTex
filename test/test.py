from jinjatex import Document, Block

doc = Document()
doc.loadTemplate("/home/ubuntu/jinjaTex/test/default.tex")
doc.Header(type='section', name='Chapter 1')
doc.Image(path="test.png", label='img1', caption="Image 1")

tableHeader = ['First', 'Second', 'Third']
rows = [
    ["row1", " Other Text", "Other Text 2"],
    ["row2", "", ""],
    ["row3", "Other Text 4", ""],
    ["row4", " Other Text 6", "Other Text"],
    ["row5", ""],
    ["row6", " Other Text 9", ""],
]

doc.Table(tableHeader, rows)
doc.blocks.append(Block(body='THIS IS SOME TEXT'))
doc.render("/home/ubuntu/output.pdf")

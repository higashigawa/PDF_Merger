import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QAbstractItemView
from PyPDF2 import PdfMerger

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('PDF Merger')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.fileList = QListWidget(self)
        self.fileList.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(self.fileList)
        
        self.addButton = QPushButton('Add PDFs', self)
        self.addButton.clicked.connect(self.add_pdfs)
        layout.addWidget(self.addButton)
        
        self.removeButton = QPushButton('Remove Selected', self)
        self.removeButton.clicked.connect(self.remove_selected)
        layout.addWidget(self.removeButton)
        
        self.mergeButton = QPushButton('Merge PDFs', self)
        self.mergeButton.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.mergeButton)
        
        self.setLayout(layout)
        
    def add_pdfs(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files to add", "", "PDF Files (*.pdf)", options=options)
        
        if files:
            for file in files:
                item = QListWidgetItem(file)
                self.fileList.addItem(item)

    def remove_selected(self):
        for item in self.fileList.selectedItems():
            self.fileList.takeItem(self.fileList.row(item))
        
    def merge_pdfs(self):
        if self.fileList.count() == 0:
            QMessageBox.warning(self, "Warning", "No files to merge.")
            return
        
        merger = PdfMerger()
        
        for i in range(self.fileList.count()):
            item = self.fileList.item(i)
            merger.append(item.text())
            
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)", options=options)
        
        if save_path:
            merger.write(save_path)
            merger.close()
            QMessageBox.information(self, "Success", "PDFs merged successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Save operation cancelled.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFMergerApp()
    ex.show()
    sys.exit(app.exec_())

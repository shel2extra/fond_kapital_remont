import csv
import os
from tqdm import tqdm
from multiprocessing import Pool
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import fitz


def save_info(list):
    with open('result.csv', 'a', encoding='utf-8', newline='') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(list)



def checker_texts(ocr_result, page_number, pdf_path, page_count):
    if 'доводч' in ocr_result.lower():
        print(f'Найдено, {pdf_path} страница - {page_number} из {page_count}')
        save_info([pdf_path, page_number])
    else:
        print(f'НЕ найдено страница {page_number} из {page_count}')


def extracter_text_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page_len = doc.page_count
    for page_number in range(page_len+1):
        page = doc[page_number]
        # Рендеринг страницы в изображение
        image = page.get_pixmap(dpi=200)
        # Сохранение изображения в формате JPG
        image_path = f"page_{page_number + 1}.jpg"
        image.save(image_path, "JPEG")
        ocr_result = tess.image_to_string(image_path, lang='rus')
        checker_texts(ocr_result, page_number, pdf_path, page_len)
        os.remove(image_path)


        # print(f"Page {page_number + 1} saved as {image_path}")

    doc.close()


if __name__ == "__main__":
    folder = os.listdir(r'C:\Users\User\Desktop\Закупки')
    for one_folder in tqdm(folder):
        folder_1 = [rf'C:\Users\User\Desktop\Закупки\{one_folder}\{x}' for x in os.listdir(
        rf"C:\Users\User\Desktop\Закупки\{one_folder}") if "кс-2" in
                    x.lower() and "фасад" in x.lower()]
        if folder_1:
            for path in tqdm(folder_1, leave=False):
                try:
                    extracter_text_in_pdf(path)
                except:
                    pass
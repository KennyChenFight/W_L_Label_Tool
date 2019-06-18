import os
from shutil import copyfile, rmtree
import traceback


class LabelTool:
    w_label_file_dir = 'w_label/'
    w_p_file_dir = 'compare/w_p/'
    l_label_file_dir = 'l_label/'
    l_p_file_dir = 'compare/l_p/'
    txt_p_file_dir = 'compare/txt/'
    wav_p_file_dir = 'compare/wav/'
    txt_o_file_dir = 'txt/'
    wav_o_file_dir = 'wav/'
    analysis_file = 'label_analysis.txt'
    compare_dir = 'compare/'

    # 分析w_lab與l_lab每個檔案不同的地方，並擷取檔案出來
    @classmethod
    def analysis_label(cls, is_mono=False, is_half_full=False):
        w_label_filepaths = os.listdir(cls.w_label_file_dir)
        l_label_filepaths = os.listdir(cls.l_label_file_dir)

        message = ''
        if len(w_label_filepaths) != len(l_label_filepaths):
            message = '檔案數量不一致'
        else:
            if is_mono:
                try:
                    w_pron_dict, l_pron_dict = cls.read_mono_file(w_label_filepaths, l_label_filepaths)
                    cls.compare_label(w_pron_dict, l_pron_dict)
                    message = '比對完成'
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    message = '比對失敗'
            elif is_half_full:
                try:
                    w_pron_dict, l_pron_dict = cls.read_half_full_file(w_label_filepaths, l_label_filepaths)
                    cls.compare_label(w_pron_dict, l_pron_dict)
                    message = '比對完成'
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    message = '比對失敗'
        return message

    # 讀取w及l的mono lab檔案
    @classmethod
    def read_mono_file(cls, w_label_filepaths, l_label_filepaths):
        w_pron_dict = {}
        for filepath in w_label_filepaths:
            with open(cls.w_label_file_dir + filepath, encoding='utf-8') as f:
                total_pron = []
                for line in f:
                    line = line.strip().split(' ')
                    pron_list = [s for s in line if s.isalpha()]
                    total_pron.extend(pron_list)
            w_pron_dict[filepath] = total_pron
        print(w_pron_dict)
        l_pron_dict = {}
        for filepath in l_label_filepaths:
            with open(cls.l_label_file_dir + filepath, encoding='utf-8') as f:
                total_pron = []
                for line in f:
                    line = line.strip().split(' ')
                    pron_list = [s for s in line if s.isalpha()]
                    total_pron.extend(pron_list)
            l_pron_dict[filepath] = total_pron
        print(l_pron_dict)
        return w_pron_dict, l_pron_dict

    # 讀取w及l的half_full lab檔案
    @classmethod
    def read_half_full_file(cls, w_label_filepaths, l_label_filepaths):
        w_pron_dict = {}
        for filepath in w_label_filepaths:
            with open(cls.w_label_file_dir + filepath, encoding='utf-8') as f:
                total_pron = []
                for line in f:
                    line = line.strip()
                    dash_index = line.find('-')
                    plus_index = line.find('+')
                    total_pron.append(line[dash_index + 1 : plus_index])

            w_pron_dict[filepath] = total_pron
        print(w_pron_dict)
        l_pron_dict = {}
        for filepath in l_label_filepaths:
            with open(cls.l_label_file_dir + filepath, encoding='utf-8') as f:
                total_pron = []
                for line in f:
                    dash_index = line.find('-')
                    plus_index = line.find('+')
                    total_pron.append(line[dash_index + 1: plus_index])

            l_pron_dict[filepath] = total_pron
        print(l_pron_dict)
        return w_pron_dict, l_pron_dict

    # 比較W及L的lab檔案，拼音不同的行數挑出來
    @classmethod
    def compare_label(cls, w_pron_dict, l_pron_dict):
        compare_message = {}
        for filename, w_pron_list in w_pron_dict.items():
            counter = 1
            compare = []
            l_pron_list = l_pron_dict[filename]
            if len(w_pron_list) > len(l_pron_list):
                l_pron_list.extend(['none'] * (len(w_pron_list) - len(l_pron_list)))
            elif len(w_pron_list) < len(l_pron_list):
                w_pron_list.extend(['none'] * (len(l_pron_list) - len(w_pron_list)))

            for x in zip(w_pron_list, l_pron_list):
                if x[0] == x[1]:
                    counter += 1
                    continue
                if x[0] != x[1]:
                    compare.append(str(counter))
                    counter += 1
            if compare:
                compare_message[filename] = compare

        print(compare_message)
        cls.check_default_dir_has_odd_data()
        cls.copy_problem_file(compare_message)
        cls.copy_txt_and_wav_file(compare_message)
        cls.write_compare_message(compare_message)

    # 檢查預設的資料夾有無舊的label檔案，有的話就刪除
    @classmethod
    def check_default_dir_has_odd_data(cls):
        for dir_path, _, _ in os.walk(cls.compare_dir):
            if os.listdir(dir_path) and dir_path != cls.compare_dir:
                rmtree(dir_path)
                os.mkdir(dir_path)

    # 將挑出來的錯誤lab檔案複製到對應的資料夾裡
    @classmethod
    def copy_problem_file(cls, compare_message):
        for filename, wrong_lines in compare_message.items():
            copyfile(cls.w_label_file_dir + filename, cls.w_p_file_dir + filename)
            copyfile(cls.l_label_file_dir + filename, cls.l_p_file_dir + filename)

    # 將錯誤的txt跟wav複製到對應的資料夾裡
    @classmethod
    def copy_txt_and_wav_file(cls, compare_message):
        for filename, _ in compare_message.items():
            txt_filename = filename.replace('.lab', '.txt')
            wav_filename = filename.replace('.lab', '.wav')
            copyfile(cls.txt_o_file_dir + txt_filename, cls.txt_p_file_dir + txt_filename)
            copyfile(cls.wav_o_file_dir + wav_filename, cls.wav_p_file_dir + wav_filename)

    # 輸出label比較訊息，挑出錯誤的行數
    @classmethod
    def write_compare_message(cls, compare_message):
        with open(cls.analysis_file, 'w', encoding='utf-8') as f:
            for filename, wrong_lines in compare_message.items():
                f.write(filename)
                f.write(',')
                f.write(','.join(wrong_lines))
                f.write('\n')
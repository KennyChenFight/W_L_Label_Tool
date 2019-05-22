import os
from shutil import copyfile

class LabelTool:
    w_label_file_dir = 'w_label/'
    w_p_file_dir = 'w_p/'
    l_label_file_dir = 'l_label/'
    l_p_file_dir = 'l_p/'
    analysis_file = 'label_analysis.txt'

    @classmethod
    def analysis_label(cls, is_mono=False, is_half_full=False):
        w_label_filepaths = os.listdir(cls.w_label_file_dir)
        l_label_filepaths = os.listdir(cls.l_label_file_dir)

        if len(w_label_filepaths) != len(l_label_filepaths):
            print('檔案數量不一致')
            return
        else:
            if is_mono:
                w_pron_dict, l_pron_dict = cls.read_mono_file(w_label_filepaths, l_label_filepaths)
                cls.compare_label(w_pron_dict, l_pron_dict)
            elif is_half_full:
                w_pron_dict, l_pron_dict = cls.read_half_full_file(w_label_filepaths, l_label_filepaths)
                cls.compare_label(w_pron_dict, l_pron_dict)
            else:
                print('choose file type')

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
        cls.copy_problem_file(compare_message)
        cls.write_compare_message(compare_message)

    @classmethod
    def copy_problem_file(cls, compare_message):
        for filename, wrong_lines in compare_message.items():
            copyfile(cls.w_label_file_dir + filename, cls.w_p_file_dir + filename)
            copyfile(cls.l_label_file_dir + filename, cls.l_p_file_dir + filename)

    @classmethod
    def write_compare_message(cls, compare_message):
        with open(cls.analysis_file, 'w', encoding='utf-8') as f:
            for filename, wrong_lines in compare_message.items():
                f.write(filename)
                f.write(',')
                f.write(','.join(wrong_lines))
                f.write('\n')
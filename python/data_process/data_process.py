def clean_ipv6(data_path, new_path):
    with open(data_path, 'r') as f1:
        with open(new_path, 'w') as f2:
            lines = f1.readlines()
            data = []
            for i in range(len(lines)):
                if not lines[i].startswith('-'):
                    data.append(lines[i])

            f2.writelines(data)


def copy(data_path, new_path):
    with open(data_path, 'r') as f1:
        with open(new_path, 'w') as f2:
            lines = f1.readlines()
            data = []
            for i in range(len(lines)):
                if len(data) > 100000:
                    break
                data.append(lines[i])

            f2.writelines(data)

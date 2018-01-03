import yaml
from collections import defaultdict

def iter_membership(resource_dict_list):
    values = ['category', 'language']
    for resource_dict in resource_dict_list:
        for item in values:
            try:
                if resource_dict[item].lower() in interests:
                    yield item, resource_dict
            except KeyError:
                print('keyerror')
                pass
            except AttributeError:
                # nonetype for item.lower()
                pass

def load_yaml(input_name):
    with open(input_name, 'r') as input:
        try:
            return yaml.load(input)
        except yaml.YAMLError as exc:
            print(exc)

def build_item_dict(yaml_list):
    split = defaultdict(list)
    for found_key, dict_found in iter_membership(yaml_list):
        split[dict_found[found_key]].append(dict_found)

    print(split.keys())

if __name__ == '__main__':
    interests = ["Javascript", "Ruby", "Java", "Python", "C#", "C", "Swift",
                 ".NET", "HTML / CSS", "Mobile / IOS", "Full-Stack Developer",
                 "Data Science", "Back-End Developer", "Front-End Developer",
                 "Cyber Security", "I.T / SysAdmin", "Web Designer",
                 "Web Developer", "Mobile / Android"
                 ]

    interests = [item.lower() for item in interests]
    build_item_dict(load_yaml('resources.yml'))
import yaml
from collections import defaultdict, namedtuple, Counter
from typing import List, DefaultDict, Dict
from fuzzywuzzy import process

MatchGroup = namedtuple('MatchGroup', ['percent', 'key', 'resource_group', 'resource_val', 'all_matches'])


def load_file(input_name: str)-> List[Dict]:
    with open(input_name, 'r') as input:
        try:
            return yaml.load(input)
        except yaml.YAMLError as exc:
            print(exc)

def unique_resources(input_list: List[Dict])-> Counter:
    keys = ['category', 'language']
    final_list = []
    for single_dict in input_list:
        for item in keys:
            if single_dict[item]:
                final_list.append(single_dict[item])

    return Counter(final_list)

def best_match(single_dict_item: dict)-> MatchGroup:
    """
    finds the best interest match for a single resource dict item
    :param single_dict_item:
    :type single_dict_item:
    :return:
    :rtype:
    """
    interests = ["Javascript", "Ruby", "Java", "Python", "C#", "C", "Swift",
                 ".NET", "HTML / CSS", "Mobile / IOS", "Full-Stack Developer",
                 "Data Science", "Back-End Developer", "Front-End Developer",
                 "Cyber Security", "I.T / SysAdmin", "Web Designer",
                 "Web Developer", "Mobile / Android"
                 ]
    keys = ['category', 'language']
    some_items = [single_dict_item[key] for key in keys]
    match_percent = 0
    dict_key = None
    interest = None
    resource_val = None
    for single_key in keys:
        if single_dict_item[single_key]:
            matched_string, percent = process.extractOne(single_dict_item[single_key], interests)

            if percent > match_percent:
                match_percent = percent
                dict_key = single_key
                interest = matched_string
                resource_val = single_dict_item[single_key]

    return MatchGroup(match_percent, dict_key, interest, resource_val, some_items)

def iter_membership(resource_dict_list: List[dict])->MatchGroup:
    for resource_dict in resource_dict_list:
        yield best_match(resource_dict)


def build_item_dict(yaml_list: List[Dict[str, str]], unique_list)-> DefaultDict[str, MatchGroup]:
    split = defaultdict(list)

    for match in iter_membership(yaml_list):
        split[match.resource_group].append(match)

    for key, values in split.items():
        for item in values:
            if int(item.percent) < 60:
                print(item)


    # for key, values in split.items():
    #     print("~~~~~~ BackEnd Database Value Best Match ~~~~~~~~")
    #     print(key)
    #     print("MATCHES")
    #     for item in values:
    #         print(item)


if __name__ == '__main__':
    loaded_yaml = load_file('resources.yml')
    unique_list = unique_resources(loaded_yaml)
    print(unique_list)
    build_item_dict(loaded_yaml, unique_list)
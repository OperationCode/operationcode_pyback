import yaml
interests = ["Javascript", "Ruby", "Java", "Python", "C#", "C", "Swift",
            ".NET", "HTML / CSS", "Mobile / IOS", "Full-Stack Developer", 
            "Data Science", "Back-End Developer", "Front-End Developer",
            "Cyber Security", "I.T / SysAdmin", "Web Designer", 
            "Web Developer", "Mobile / Android"
            ]

interests = [item.lower() for item in interests]

loaded = None
with open('resources.yml', 'r') as input:
    try:
        loaded = yaml.load(input)
    except yaml.YAMLError as exc:
        print(exc)

segmented = []
for item in loaded:
    if item['category'].lower() or item['language'].lower() in interests:
        segmented.append(item)
    else:
        print(item)



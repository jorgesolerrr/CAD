

def make_params(wstoken: str, wsfunction: str, moodlewsrestformat : str = "json") -> dict:
    return {
        "wstoken": wstoken,
        "wsfunction": wsfunction,
        "moodlewsrestformat": moodlewsrestformat,
    }

def get_differences(enrolledStudents : list):
    result = [[] for i in range(len(enrolledStudents))]
    for i in range(len(enrolledStudents)):
        for j in range(len(enrolledStudents)):
            if i == j: continue
            interc = enrolledStudents[i][1].intersection(enrolledStudents[j][1])
            if len(interc) == 0:
                result[i].append(j)


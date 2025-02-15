import json
import csv



test = False

train_nummatches = [129, 130, 130, 129]
#83, 74, 66, 80,
test_nummatches = [70, 74, 86, 68]
data_event = "train"
nummatches = train_nummatches

if (test):
    nummatches = test_nummatches
    data_event = "test"




with open(f"events_data_{data_event}_locals.json", "r") as file:
    events_data = json.load(file)

with open(f"teams_data_{data_event}_locals.json", "r") as file:
    teams_data = json.load(file)

finalDict = {}
eventNum = 1

if events_data:

    numMatches = 0
    for match in events_data:
        if match == "stop":
            continue
        if match["comp_level"] != 'qm':
            continue
        numMatches += 1

    matches = []
    for i in range(0, numMatches):
        matches.append(0)


    for match in events_data:
        if match == "stop":
            eventNum += 1
            continue
        if match["comp_level"] != 'qm':
            continue

        matchnum = int(match["match_number"])
        matchdata = [matchnum]
        for team in match["alliances"]["blue"]["team_keys"]:
            matchdata.append(team)
        for team in match["alliances"]["red"]["team_keys"]:
            matchdata.append(team)
        a = (match["score_breakdown"]["blue"]["totalPoints"])
        b = (match["score_breakdown"]["red"]["totalPoints"])
        matchdata.append(a)
        matchdata.append(b)
        matchdata.append(match["score_breakdown"]["blue"]["rp"])
        matchdata.append(match["score_breakdown"]["red"]["rp"])
        matchdata.append(match["score_breakdown"]["blue"]["autoPoints"])
        matchdata.append(match["score_breakdown"]["red"]["autoPoints"])
        matchdata.append(match["score_breakdown"]["blue"]["linkPoints"])
        matchdata.append(match["score_breakdown"]["red"]["linkPoints"])
        matchdata.append(match["score_breakdown"]["blue"]["endGameChargeStationPoints"])
        matchdata.append(match["score_breakdown"]["red"]["endGameChargeStationPoints"])

        result = 0
        if(a - b > 0):
            result = 1
        if(a == b):
            result = 2

        matchdata.append(result)
        matchdata.append(eventNum)

        temp_num = nummatches
        add = 0
        if(eventNum > 1):
            for i in range(0, eventNum - 1):
                add += nummatches[i]

        matches[matchnum - 1 + add] = matchdata

if teams_data:
    avgsDict = {}
    for team in teams_data:
        if team == "stop":
            continue
        avgsDict[team['key']] = [0, 0, 0, [], 0, 0, 0]

important = []

evtracker = 1

for i in range(0, len(matches)):

    currentMatch = matches[i][0]

    if matches[i][18] != evtracker:
        evtracker += 1
    if(currentMatch > 29):
        expectedScoreDiff = 0
        expectedRpDiff = 0
        expectedAutoDiff = 0
        lastFive = 0
        linkP = 0
        endgame = 0

        for j in range(1, 7):
            diff = 1
            if(j > 3):
                diff = -1
            teamInfo = avgsDict[matches[i][j]]

            expectedScoreDiff += (diff * teamInfo[0])
            expectedRpDiff += (diff * teamInfo[1])
            expectedAutoDiff += (diff * teamInfo[2])
            if(len(teamInfo[3]) == 0):
                teamLastFive = 0
            else:
                teamLastFive = sum(teamInfo[3])/len(teamInfo[3])
            lastFive += (diff * teamLastFive)
            linkP += (diff * teamInfo[4])
            endgame += (diff * teamInfo[5])

        result = matches[i][17]
        if result == 2:
            result = 0
        importantInfo = [currentMatch, round(expectedScoreDiff, 2), round(expectedRpDiff, 2), round(expectedAutoDiff, 2), round(lastFive, 2) * 5, round(linkP, 2), round(endgame, 2), result, matches[i][18]]
        important.append(importantInfo)


    for j in range(1, 7):
        red = 0
        if(j > 3):
            red = 1
        teamInfo = avgsDict[matches[i][j]]

        newTeamInfo = [0, 0, 0, 0, 0, 0, 0]
        newTeamInfo[0] = round((teamInfo[0] * teamInfo[6] + matches[i][7 + red]) /(teamInfo[6] + 1), 2)
        newTeamInfo[1] = round((teamInfo[1] * teamInfo[6] + matches[i][9 + red]) / (teamInfo[6] + 1), 2)
        newTeamInfo[2] = round((teamInfo[2] * teamInfo[6] + matches[i][11 + red]) / (teamInfo[6] + 1), 2)
        newTeamInfo[4] = round((teamInfo[4] * teamInfo[6] + matches[i][13 + red]) / (teamInfo[6] + 1), 2)
        newTeamInfo[5] = round((teamInfo[5] * teamInfo[6] + matches[i][15 + red]) / (teamInfo[6] + 1), 2)

        temp = teamInfo[3]
        if(red == 1):
            if(matches[i][17] == 1):
                temp.append(0)
            else:
                temp.append(1)
        else:
            temp.append(matches[i][17])

        if(len(temp) > 5):
            temp.pop(0)
        newTeamInfo[3] = temp

        newTeamInfo[6] = teamInfo[6] + 1
        avgsDict[matches[i][j]] = newTeamInfo

important2 = []
important2.append(["matchNum", "scoreDiff", "rpDiff", "autoDiff", "lastFive", "linkPoints", "endgamePoints", "bluewin", "eventNum"])
for i in range(0, len(important)):
    for j in range(1, 6):
        important[i][j] = round(important[i][j], 2)
    important2.append(important[i])

with open(f"worlds_{data_event}.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(important2)

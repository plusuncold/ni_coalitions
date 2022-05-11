from itertools import combinations
from colorama import Fore, Back, Style

parties = {
    "Sinn Féin": [27, "O'Neill", "N", 250388],
    "DUP": [25, "Donaldson", "U", 184002],
    "Alliance": [17, "Long", "O", 116681],
    "UUP": [9, "Beattie", "U", 96390],
    "SDLP": [8, "Eastwood", "N", 78237],
    "TUV": [1, "Allister", "U", 65788],
    "PBP": [1, "McCann", "O", 9798],
    "Alex Easton": [1, "Easton", "U", 9568],
    "Claire Sugden": [1, "Sudgen", "U", 3981]
}
majority = sum([ x[0] for x in parties.values() ]) // 2 + 1
independents = [ x for x in parties if parties[x][0] == 1]


def get_color(party):
    designation = parties[party][2]
    if designation == "N":
        return Fore.GREEN
    if designation == "U":
        return Fore.RED
    return Fore.WHITE


def get_minister(party):
    minster_name = parties[party][1]
    return get_color(party) + minster_name + Fore.WHITE

def get_executive(coalition):
    executive_dict = {}
    executive_designation = { "N": 0, "U": 0, "O": 0 }
    for party in coalition:
        executive_dict[party] = 0
    executive = ""
    
    while sum(executive_dict.values()) < 9:
        party_seats_adjusted_by_quota = {}
        party_first_pref_votes_adjusted_by_quota = {}

        for party in coalition:
            party_seats_adjusted_by_quota[party] = parties[party][0] / (1 + executive_dict[party])
            party_first_pref_votes_adjusted_by_quota[party] = parties[party][3] / (1 + executive_dict[party])
        
        max_quota_adjusted_seats = [key for key, value in party_seats_adjusted_by_quota.items() 
                                    if value == max(party_seats_adjusted_by_quota.values())]
        max_quota_adjusted_first_pref_votes = [key for key, value in party_first_pref_votes_adjusted_by_quota.items() 
                                               if value == max(party_first_pref_votes_adjusted_by_quota.values()) and key in max_quota_adjusted_seats]
        
        if len(max_quota_adjusted_seats) == 1:
            executive_dict[max_quota_adjusted_seats[0]] += 1
        else:
            executive_dict[max_quota_adjusted_first_pref_votes[0]] += 1

    for party in executive_dict:
        if executive_dict[party] == 0:
            continue
        executive += get_color(party) + party + ": " + str(executive_dict[party]) + " " + Style.RESET_ALL
        designation = parties[party][2]
        executive_designation[designation] += executive_dict[party]
    
    return executive, executive_designation

def get_seat_count(combination_of_parties):
    count = 0
    for party in combination_of_parties:
        count += parties[party][0]
    return count

def valid_coalition(combination_of_parties):
    seat_count = get_seat_count(combination_of_parties)

    if seat_count < majority:
        return False
    if "Sinn Féin" in combination_of_parties and "TUV" in combination_of_parties:
        return False
    #if "DUP" in combination_of_parties:
    #    return False

    # exclude coalitions with more independents than needed to make a majority
    independents_in_coalition = [ x for x in combination_of_parties if x in independents ]
    if independents_in_coalition and seat_count > majority:
        return False

    return True

possible_coalitions = []

for number_parties in range(len(parties) + 1):
    for combination in combinations(parties.keys(), number_parties):
        if valid_coalition(combination):
            possible_coalitions.append(combination)

print("Possible coalitions with a majority (" + str(majority) + "+ seats):")

for coalition in possible_coalitions:
    seat_count = get_seat_count(coalition)
    executive, executive_designation = get_executive(coalition)
    if executive_designation["N"] < 1 or executive_designation["U"] < 1:
        continue
    print(seat_count, end=" seats - ")
    party_list = ""
    for party in coalition:
        party_list += get_color(party) + party + Style.RESET_ALL + ", "
    ministers = get_minister(coalition[0]) + " " +  get_minister(coalition[1])
    print(party_list[:-2] + "\t\tFirst Minsters:", ministers,"\tExecutive:", executive, "+ Justice")


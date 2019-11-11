from itertools import permutations

# import from itertools the ability to find permutations
# define function called balanceable, that accepts one parameter which is called numbers and is a list of integers


def balanceable(numbers):

    # take the list of integers that we receive as the parameters and store it in a variable called num_list
    num_list = numbers

    # make a list of all the possible permutations of the list num_list and store it in variable l
    l = list(permutations(num_list))

    # find the sum of the entire list of numbers that we receive as parameters and store it in variable final_sum
    # Then take that final_sum value and divide it by 2 to get the half sum
    # half_sum will be what we want one side to equal because if it equals one side it must equal the other side
    final_sum = sum(num_list)
    half_sum = final_sum/2

    # set a dummy variable of teeter to false to start
    teeter = False

    # loop through every possible permutation of num_list
    # loop through every element in num_list which is the total number of elements in numbers
    # WE are going to look at the all the pieces of f include l[i][0] to l[i][n]
    # if the sum of those elements equals half sum then we set teeter to true
    for i in range(len(l)):
        for n in range(len(num_list)):
            f = l[i][0: 0+n]
            if sum(f) == half_sum:
                teeter = True

    # Based on what we found previously if teeter has changed to true return true and the list is balancable
    # if the teeter remains false return false and the list is not balancable
    if teeter == True:
        print("True")
        return True
    else:
        print("False")
        return False
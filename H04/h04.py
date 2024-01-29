import sys
import heapq

input = open(sys.argv[1], 'r', encoding='utf-8')

# input = input.split('\n')

def polyhash(line, x, m):
	hashsum = 0

	for i in range(len(line)):
		hashsum = (hashsum * x + ord(line[i])) % m
	return hashsum

m_hl = 2 ** 63 # use this value of m for the hyperloglog.
m_cm = 2800 # for count-min sketch

x_hl = 128109 # for unique integer from string used in the hyperlogog algorithm
x_cm = [171043, 2334107, 6913139, 77543, 1997753] # for five count-min array

# Array holding the buckets for the hyperloglog estimate values
bucket_array = [0, 0, 0, 0, 0, 0, 0, 0]

# Initializing arrays for each hash function
a1 = [0] * m_cm
a2 = [0] * m_cm
a3 = [0] * m_cm
a4 = [0] * m_cm
a5 = [0] * m_cm

# Initializing the min priority queue
min_pq = []
# Map of currently active tags
active_tags = {}

# For every line in the input
for line in input:
    # Check that line in not empty, first character is @, #, or quotation mark, and if a quation mark the second character is @ or # 
    if line[0] == "@":

        ### First process the HyperLogLog estimate
        # Get the hash number of the hashtag
        hash = polyhash(line, x_hl, m_hl)
        # Convert the hash to binary
        binary = bin(hash)

        # Count the number of trailing zeros (starting at 1 is somehow closer to the correct value)
        tzeros = 1
        while binary[len(binary) - 1] == '0':
            binary = binary[:len(binary) - 1]
            tzeros += 1

        # Removes trailing 1 from the binary value
        binary = binary[:len(binary) - 1]

        # If the binary value was somehow completely removed, translates the value to 0
        if (binary == '0b'):
            bucket = 0
        # Otherwise, gets the value of the last three digits for the bucket
        else:
            bucket = int(binary, 2) & 7

        # Goes to the bucket index, and puts the maximum trailing zero value in (either original value or current tzeros)
        bucket_array[bucket] = max(tzeros, bucket_array[bucket])

        ### Second process the count-min sketch and min priority queue
        # Calculates hash indexes for each array
        h1 = polyhash(line, x_cm[0], m_cm)
        h2 = polyhash(line, x_cm[1], m_cm)
        h3 = polyhash(line, x_cm[2], m_cm)
        h4 = polyhash(line, x_cm[3], m_cm)
        h5 = polyhash(line, x_cm[4], m_cm)

        # Increments hashed indexes in the arrays
        a1[h1] += 1
        a2[h2] += 1
        a3[h3] += 1
        a4[h4] += 1
        a5[h5] += 1

        # Gets the minimum value out of each of the array positions
        curr_freq = min( a1[h1], a2[h2], a3[h3], a4[h4], a5[h5] )

        # If tag is already in the list
        if active_tags.get(line):
            # With an empty heap, builds from the current min_pq heap until the tag is found
            temp_heap = []
            min_freq = heapq.heappop( min_pq )
            while min_freq[1] != line:
                heapq.heappush( temp_heap, min_freq )
                min_freq = heapq.heappop( min_pq )
            # Desired tag is found and pushed into temp_heap with new frequency
            heapq.heappush( temp_heap, (curr_freq, line) )
            # Remainder of heap is consolidated, either back onto original or temp depending on which is bigger
            if len(temp_heap) > len(min_pq):
                while len(min_pq) > 0:
                    heapq.heappush( temp_heap, heapq.heappop( min_pq ) )
                min_pq = temp_heap
            else:
                while len(temp_heap) > 0:
                    heapq.heappush( min_pq, heapq.heappop( temp_heap ) )
        # Tag is not already in the list
        else:
            # If length of list is still less than 100, simply add it to the list and map
            if len(min_pq) < 100:
                heapq.heappush( min_pq, (curr_freq, line) )
                active_tags[line] = curr_freq
            else:
                # List is full, pop the minimum value
                min_freq = heapq.heappop( min_pq )
                # If the min value is greater than the current frequency, put the min back in and ditch the current
                if ( min_freq[0] > curr_freq ):
                    heapq.heappush( min_pq, min_freq )
                # New frequency replaces the min, old min is removed from the map, and the new frequency is added to the map and list
                else:
                    del active_tags[min_freq[1]]
                    heapq.heappush( min_pq, (curr_freq, line) )
                    active_tags[line] = curr_freq

# Calculates the harmonic means
h = 0
for i in bucket_array:
    h += (1 / pow(2, i))
h = 8 / h

# Calculates hyperloglog estimate
est_D = 8 * h / 0.77351

# Printing estimate number of hashtags
print("The hyperloglog estimate is " + str(round(est_D)))

# Printing the top 100 tags
# Pops the tags into an array
tags = []
while len(min_pq) > 0:
     tags.append(heapq.heappop(min_pq))

# Prints the popped tags in reverse order, so from highest to lowers
for i in reversed(tags):
    print(str(i[0]) + " " + i[1], end="")

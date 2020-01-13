=begin
# a
a = gets.to_i
b = gets.to_i

for i in 1..3 do
  if i != a and i != b
    puts i
    break
  end
end
=end

=begin
# b
N = gets.to_i
words = gets.split(' ')
answer = ""
for i in 0..N-1 do
  words.each do |w|
    answer += w[i]
  end
end

puts answer
=end

# c
=begin
A, B = gets.split(' ')
a = A.to_i
b = B.to_i

lcm = a # 最小公倍数
i = 1
while true
  lcm = a * i      # lcmをaの2倍,3倍,・・・i倍にしていく
  if lcm % b == 0  # lcmがbの倍数（bで割った余りが0）になったら繰り返しを打ち切る
    break
  else
    i += 1
  end
end
puts lcm
=end

# d
=begin
N = gets.to_i
nums = gets.split(' ').map(&:to_i)

cnt = 0
mark = 1
nums.each do |n|
  if n == mark
    cnt += 1
    mark += 1
  end
end
if cnt == 0
  puts -1
else
  puts (nums.length - cnt)
end
=end

# e
include Math
N = gets.to_i
if N % 2 == 1
  puts 0
else
  order = Math.log(N, 5)
  # puts order
  ans = 0
  (1..order).each do |i|
    ans += N.div(5**i)/2
    #print i.to_s + " "
    #puts ans
  end
  puts ans
end
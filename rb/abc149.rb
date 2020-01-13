=begin
#A
ST = gets.split(' ').reverse!

ST.each do |st|
  print st
end
=end

#B
=begin
A,B,K = gets.split(' ').map(&:to_i)
a = [A-K,0].max
b = [0,B + [A-K,0].min].max

print a
print ' '
print b
=end 

#C
=begin
require 'prime'
x =  gets.to_i
puts Prime.find {|p| p >= x }
=end

#D
=begin
N,K = gets.split(' ').map(&:to_i)
R,S,P = gets.split(' ').map(&:to_i)
T = gets

arrays = Array.new
K.times do
  arrays << Array.new
end

i = 0
N.times do
  arrays[i%K].push(T[i])
  i += 1
end

score = 0
arrays.each do |arr|
  arr.size.times do |i|
    if i!=0 and arr[i]==arr[i-1]
      arr[i]='x'
    else
      if arr[i]=='r'
        score += P
      elsif arr[i]=='s'
        score += R
      else
        score += S
      end
    end
  end
end

print score
=end

#E
# 作業中
class Array
  def count
    k = Hash.new(0)
    self.each{|x| k[x] += 1 }
    return k
  end
end

N,M = gets.split(' ').map(&:to_i)
A = gets.split(' ').map(&:to_i)
a = A.count
m = M

#p a
unkey = a.keys.sort.reverse
candidates = []
# key_idx = Array.new(unkey.size,0)

(0...unkey.size).each do |i|
  candidates << [i, i, unkey[i]+unkey[i]]
end
#p unkey
#p candidates
score=0
while m > 0
  #print 'm='
  #puts m
  #p unkey[candidates[0][0]]
  x =  unkey[candidates[0][0]] + unkey[candidates[0][1]]
  #p x
  m1 = a[unkey[candidates[0][0]]] * a[unkey[candidates[0][1]]]
  if candidates[0][0] != candidates[0][1]
    m1 *= 2
  end
  combs = [m,m1].min
  #print 'combs '
  #puts combs
  # 先頭（最大値）を取ってくる


  score += candidates[0][2] * combs 
  m -= combs
  
  #print 'score '
  #puts score
  # 先頭の更新
  #print '先頭の更新 '
  #puts candidates[0][1]
  candidates[0][1] += 1
  
  if candidates[0][1] >= unkey.size
    candidates = candidates.slice(1...unkey.size)
  else
    candidates[0][2] = unkey[candidates[0][0]] + unkey[candidates[0][1]] 
    if candidates[0][2] < candidates[1][2]
      # 先頭を取り出す
      tmp = candidates[0]
      i = 1
      while tmp[2] < candidates[i][2]
        i+=1
      end  
      candidates = candidates.slice(1..i-1)+[tmp]+candidates.slice(i...unkey.size)
    end
  end
  
  #p candidates
end  

p score
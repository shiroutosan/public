# Programing Ruby の実行テスト用

puts "ああああ"
a = 5
var = if a < 5
        'a'
      else 'b'
      end
puts var

# メソッドのリネームのテスト
class Test1
    def method1(var1)
        puts var1
    end
end

class Test2 < Test1
    alias method2 method1 # メソッドのリネーム
end

t2 = Test2.new()
t2.method2('XXX')
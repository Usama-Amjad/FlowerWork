# Ruby program to demonstrate 
# the case statement with range

print "Enter number: ";
num = gets.chomp.to_i;  

case num
when 1..5
   puts "Input number is within the range of 1 to 5"; 
when 6..10
   puts "Input number is within the range of 6 to 10"; 
when 11..15
   puts "Input number is within the range of 11 to 15"; 
when 16..20
   puts "Input number is within the range of 16 to 20"; 
when 21..25
   puts "Input number is within the range of 21 to 25"; 
else
    puts "Unknown number";    
end
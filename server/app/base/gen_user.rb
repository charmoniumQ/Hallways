if ARGV.count != 1
  p 'rails console gen_user.rb [USERNAME]'
else
  username = ARGV[0]
  alphabet = ('a'..'z').to_a + ('A'..'Z').to_a + ('0'..'9').to_a
  token = ''
  30.times do
    token += alphabet.sample
  end

  u = User.find_by(username: username)
  if not u.nil?
    u.delete
  end

  User.create(username: username, password: token, password_confirmation: token)
  File.open('secure/password.txt', 'a') { |file|
    file.write("#{username} #{token}")
  }
end

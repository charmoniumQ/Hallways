if (ARGV.count != 1 or not Dir.getwd.ends_with?('rails_server')) and ARGV.count != 2
  p 'rails runner app/base/gen_user.rb USERNAME [FILE]'
  p 'If no FILE is passed, make sure that you are in the directory project_root/rails_server and project_root/resources/private exists'
  p 'In that case, the passwords will be written to ../resources/private/password.txt'
else
  file_name = (ARGV.count == 1 ? '../resources/private/password.txt' : ARGV[1])
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
  File.open(file_name, 'a') do |file|
    file.write("#{username} #{token}\n")
  end
end

require 'net/http'
require 'json'

if (ARGV.count == 0 and not Dir.getwd.ends_with?('rails_server')) and ARGV.count == 1
  p 'rails runner app/base/test_server.rb [FILENAME]'
  p 'If no file is supplied, you must run this from project_root/rails_server and ../resources/private/passwords.txt must be filled'
  abort
end

username = ''
token = ''
file_name = (ARGV.count == 0 ? '../resources/private/password.txt' : ARGV[0])
File.open(file_name, 'r') do |f| 
  data = f.readline.split(' ')
  username = data[0]
  token = data[1]
end

def test(input, expected_output)
  uri = URI.parse('http://localhost:3000/upload')
  http = Net::HTTP.new(uri.host, uri.port)
  res = http.post(uri.path, input)
  output = res.body
  if res.body != expected_output
    p 'INCORRECT'
    p "#{input} => #{output} != #{expected_output}"
  else
    #p "#{input} => #{output}"
  end
end

# not JSON
test(
  'not json text',
  '{"status":1,"error":"Invalid JSON format"}'
)

# wrong username
test(
  {'username' => username + 'f', 'token' => token}.to_json,
  '{"status":2,"error":"Invalid authentication"}'
)

# wrong token
test(
  {'username' => username, 'token' => token + 'f'}.to_json,
  '{"status":2,"error":"Invalid authentication"}'
)

# no fingerprint JSON, but good authentication
test(
  {'username' => username, 'token' => token}.to_json,
  '{"status":3,"error":"Invalid fingerprint JSON"}'
)

# all correct
test(
  {'username' => username, 'token' => token, 'fingerprints' => [{"x" => 0.1, "y" => 0.2, "z" => 0.3, "n" => 100, "stddev" => 2, "avg" => 40, "bssid" => "awle"}]}.to_json,
  '{"status":0}'
)

# extra param
test(
  {'username' => username, 'token' => token, 'fingerprints' => [{"x" => 0.1, "y" => 0.2, "z" => 0.3, "n" => 100, "stddev" => 2, "avg" => 40, "bssid" => "awle", "extra" => "tewh"}]}.to_json,
  '{"status":3,"error":"Invalid fingerprint JSON"}'
)

# one less param
test(
  {'username' => username, 'token' => token, 'fingerprints' => [{"x" => 0.1, "y" => 0.2, "z" => 0.3, "n" => 100, "stddev" => 2, "avg" => 40}]}.to_json,
  '{"status":3,"error":"Invalid fingerprint JSON"}'
)

# one bad one good
test(
  {'username' => username, 'token' => token, 'fingerprints' => [{"x" => 0.1, "y" => 0.2, "z" => 0.3, "n" => 100, "stddev" => 2, "avg" => 40, "bssid" => "awle"}, {"x" => 0.1, "y" => 0.2, "z" => 0.3, "n" => 100, "stddev" => 2, "avg" => 40, "bssid" => "awle", "extra" => "tewh"}]}.to_json,
  '{"status":3,"error":"Invalid fingerprint JSON"}'
)

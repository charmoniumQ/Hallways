gem install rails

rails new server --skip-test-unit --skip-javascript --api
cd server

read -p "Change the gem file and press enter "
# add devise, rails, bcrypt, and sqlite3
bundle install

rails generate model Fingerprint bssid:string x:float y:float z:float avg:float stddev:float n:integer, n:integer
rails generate model User username:string password_digest:string
rake db:drop db:create db:migrate

read -p "Edit app/model/* and app/base/* and press enter "
rails runner app/base/gen_user.rb main

rails generate controller api_auth
rails generate controller main upload download
rm -rf app/assets app/helpers app/mailers app/views secure/

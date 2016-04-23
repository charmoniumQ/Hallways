class Fingerprint < ActiveRecord::Base
  has_many :networks
  validates :x, :y, :z, :n, :bssid, presence: true
end

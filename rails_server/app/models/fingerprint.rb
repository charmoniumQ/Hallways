class Fingerprint < ActiveRecord::Base
  validates :x, :y, :z, :avg, :stddev, :n, :bssid, presence: true
end

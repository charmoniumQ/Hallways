class Fingerprint < ActiveRecord::Base
  validates :bssid, :x, :y, :z, :avg, :stddev, :n, presence: true
end

class Fingerprint < ActiveRecord::Base
  validates :bssid, :x, :y, :avg, :stddev, :n, presence: true
end
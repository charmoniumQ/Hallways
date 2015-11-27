class CreateFingerprints < ActiveRecord::Migration
  def change
    create_table :fingerprints do |t|
      t.string :bssid
      t.float :x
      t.float :y
      t.float :avg
      t.float :stddev
      t.integer :n

      t.timestamps null: false
    end
  end
end

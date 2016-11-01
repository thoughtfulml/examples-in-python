require 'csv'
require 'dalli'
require 'geocoder'

require 'pry'

Geocoder.configure(:lookup => :bing, :api_key => " AjLDV1xNmvz45hsnvPuISVI8hjFrSYkjxij3AcJMShIzYNh25fL7QhkYA_Te3_hJ")

dc = Dalli::Client.new('localhost:11211')
headers = nil
count = 0

dictionary = {}

IGNORE_HEADERS = %w[id TaxableValue Address ErosionHazard LandfillBuffer HundredYrFloodPlain SeismicHazard LandslideHazard SteepSlopeHazard Stream Wetland SpeciesOfConcern SensitiveAreaTract AirportNoise DNRLease CommonProperty CoalMineHazard CriticalDrainage]

CSV.open('./king_county_data_geocoded.csv', 'wb') do |csv|
  CSV.foreach('/tmp/king_county_data.csv', headers: true) do |row|
    headers ||= begin 
                  headers = row.headers.reject {|h| IGNORE_HEADERS.include?(h) } + ['lat', 'long']
                  csv << headers
                  headers
                end

    binary = ->(x) {
      if x == 'N'
        0
      elsif x == 'Y'
        1
      else
        x
      end
    }

    if count % 9 == 0
      response = nil
      if response = dc.get(row['id'])
      else
        sleep 0.25
        response = Geocoder.search(row['Address'])
        if response.empty?
          print "Nothing back from Bing"
          count += 1
          next
        else
          dc.set(row['id'], response.first.coordinates)
        end
      end
      puts count
    
      lat, long = response
      if response && row['AppraisedValue'].to_f < 1_000_000 && row['AppraisedValue'].to_f > 10_000

        r = []

        row.to_hash.each do |k,v|
          if IGNORE_HEADERS.include?(k)

          else
            r << binary.(v)
          end
        end

        r += [lat, long] 
        csv << r
      end
    end
    count += 1

  end
end

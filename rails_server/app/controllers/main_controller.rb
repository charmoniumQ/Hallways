require 'json'

class MainController < ApplicationController
  def upload
    handle_error do
      begin
        if @req['fingerprints'].nil? or not @req['fingerprints'].kind_of?(Array)
          raise ArgumentError
        end
        model_objs = @req['fingerprints'].collect do |raw_obj|
          model_obj = Fingerprint.new(raw_obj)
          raise ArgumentError if model_obj.invalid?
          model_obj
        end
      rescue ActiveRecord::UnknownAttributeError, ArgumentError
        logger.info {"#{@user.username}: invalid fingerprint JSON: #{@body}"}
        render json: {'status': 3, 'error': 'Invalid fingerprint JSON'}
      else
        model_objs.each do |f|
          f.save
        end
        update_response(model_objs)
        render json: {'status': 0}
      end
    end
  end

  def download
    handle_error do
      update_response(nil) # ensures that the response exists
      render json: {'status': 0, 'data': @@response}
    end
  end

  def update_response(fs)
    unless defined? @@response
      # build from scratch
      @@response = []
      update_response(Fingerprint.find_each)
    end
    unless fs.nil?
      # build by modifying previous one to include fs
      fs.each do |f| 
        @@response << {'x': f.x, 'y': f.y, 'z': f.z, 'avg': f.avg}
      end
    end
  end
end

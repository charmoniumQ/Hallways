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
      update_response(nil) unless defined? @@response
      render json: {'status': 0, 'data': @@response.to_json}
    end
  end

  def update_response(new_fingerprint)
    if new_fingerprint.nil?
      @@response = []
      Fingerprint.find_each do |f|
        update_response(f)
      end
    else
      @@response << {'x': f.x, 'y': f.y, 'z': f.z, 'avg': f.avg}
    end
  end
end

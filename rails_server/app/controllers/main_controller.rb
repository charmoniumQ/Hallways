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
      render json: {'status': 0, 'response': @@response}
    end
  end

  def update_response(new_fingerprint)
    @@response = {'quantity': 0}
    Fingerprint.find_each do |f|
      @@response[:quantity] += 1      
    end
  end
end

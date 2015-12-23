require 'json'

class MainController < ApiAuthController
  def upload
    handle_error do
      begin
        raise ArgumentError if @req['fingerprint'].nil?
        new_fingerprint = Fingerprint.new(@req['fingerprint'])
        raise ArgumentError if new_fingerprint.invalid?
      rescue ActiveRecord::UnknownAttributeError, ArgumentError
        logger.info {"#{user.username}: invalid fingerprint JSON: #{@body}"}
        render json: {'status': 3, 'error': 'Invalid fingerprint JSON'}
      else
        new_fingerprint.save
        update_response(new_fingerprint)
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

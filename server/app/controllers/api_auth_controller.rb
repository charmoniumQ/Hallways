require 'json'

class ApiAuthController < ApplicationController
  skip_before_filter :verify_authenticity_token
  before_filter :parse_request!, :authenticate_user_from_token!

  # Explicit error handling should still be done locally when:
  #     - Open resources need to be cleaned up before termination
  #     - Expected errors
  def handle_error(&block)
    begin
      block.call
    rescue => e
      logger.error {"Unknown internal error: #{exc_to_s(e)}"}
      render json: {'status': 4, 'error': 'Unknown internal error'}
    end
  end

  private
  def authenticate_user_from_token!
    handle_error do
      t1 = Time.now
      @user = nil
      if @req.has_key?('username') and @req.has_key?('token')
        tmp = User.find_by(username: @req['username'])
        if not tmp.nil?
          @user = tmp.authenticate(@req['token'])
        end
      end
      if !@user
        ensure_delay(t1, 0.5)
        # sleep for 0.5 seconds since t1 to prevent timing attacks
        # the time of exit would otherwise leak whether or not the username was found in the database
        render json: {'status': 2, 'error': 'Invalid authentication'}
      end
    end
  end

  def parse_request!
    handle_error do
      @body = request.body.read
      begin
        @req = JSON.parse(@body)
      rescue JSON::ParserError
        logger.debug {"Invalid JSON: #{@body}"}
        render json: {'status': 1, 'error': 'Invalid JSON format'}
      end
    end
  end
end

def exc_to_s(e)
  return "#{e.backtrace.first}: #{e.message} (#{e.class})\n" + e.backtrace.drop(1).map{|s| "\t#{s}\n"}.join
end

def ensure_delay(t1, delay_time)
  t2 = Time.now
  if t1 - t2 + delay_time > 0
    sleep(t1 - t2 + delay_time)
  end
end

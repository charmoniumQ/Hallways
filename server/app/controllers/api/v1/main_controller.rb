require 'json'

class Api::V1::MainController < ApplicationController
  skip_before_filter :verify_authenticity_token, :if => Proc.new { |c| c.request.format == 'application/json' }
  before_action :authenticate

  def upload
    begin
      begin
        input_params = JSON.parse(request.body.read)
        new_fingerprint = Fingerprint.new(input_params)
        puts input_params
        puts new_fingerprint
        raise ArgumentError.new('invalid fingerprint') unless new_fingerprint.valid?
      rescue JSON::ParserError, ActiveRecord::UnknownAttributeError
        render json: {'status': 1, 'error': 'Invalid request'}
      else
        new_fingerprint.save
        update_response(new_fingerprint)
        render json: {'status': 0}
      end
    rescue => e
      puts e
      puts e.backtrace.join("\n")
      render json: {'status': 2, 'error': 'Unknown internal error in Api::V1::MainController.upload'}
    end
  end

  def download
    begin
      build_response unless defined? @@response
      render json: @@response
    rescue
      render json: {'status': 2, 'error': 'Unkown internal error in Api::V1::MainController.download'}
    end
  end

  private

  def build_response
    puts "building"
    @@response = {'status': 0, 'quantity': 0}
    for f in Fingerprint.all.order(:created_at) do
      update_response(f)
    end
  end

  def update_response(new_fingerprint)
    build_response unless defined? @@response
    # TODO: update response to include new fingerprint f
    @@response[:quantity] += 1
  end

  def authenticate
    # TODO: authentication (HTTP digest or SSL?)
  end
end

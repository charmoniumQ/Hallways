Rails.application.routes.draw do
  post 'download', to: 'main#download'
  post 'upload', to: 'main#upload'
end

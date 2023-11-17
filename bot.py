import telebot
import requests
import json
import io
from bs4 import BeautifulSoup
import html

# Set up your environment variables
bot_token = '6656299533:AAEPQ2l-FbX8BoWYrLRTwizzJ6WUEiZQ6jM'

encode_api_url = 'https://base64.apinepdev.workers.dev/?encode='
decode_api_url = 'https://base64.apinepdev.workers.dev/?decode='

# MADE BY NEP CODER(@SH0NU)
bot = telebot.TeleBot(bot_token)

# MADE BY NEP CODER(@SH0NU)
tutorials = {
    '/start': '👋 Start the bot and get a welcome message.',
    '/ask': '💬 Ask a question, and the bot will try to provide an answer.',
    '/image': '🖼️ Request an image related to a text query.',
    '/photo': '📷 Convert a photo to an image URL.',
    '/hindijokes': '😄 Generate Hindi jokes.',
    '/meme': '😂 Generate memes.',
    '/quote': '💡 Generate quotes.',
    '/note': '📝 Create notes in a note-like format.',
    '/scrape': '🌐 Scrape HTML content from a website.',
    '/short': '🔗 Shorten a URL.',
    '/qr': '📲 Generate a QR code from the provided text or URL.',
    '/screenshot': '📸 Take a screenshot of a web page. Usage: /screenshot https://example.com',
    '/userinfo': '👤 Get information about a user.',
    '/weather': '☁️ Get weather information for a city. Usage: /weather cityname',
    '/encode': '🔒 Encode text using base64.',
    '/decode': '🔓 Decode base64 encoded text.'
}

# MADE BY NEP CODER(@                                                                                         )


@bot.message_handler(commands=['help'])
def help(message):
    if is_member_of_channel(message.from_user.id):
        help_text = "Available commands:\n"
        for command, description in tutorials.items():
            help_text += f"{command} - {description}\n"
        bot.reply_to(message, help_text)
    else:
        bot.reply_to(message, "You must join the channel @SH0NU_TOOLS to use this bot.")

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "👋 Hello! I am your versatile bot. How can I assist you today? Type /help to see available commands.")

@bot.message_handler(commands=['ask'])
def ask_command(message):
    user_input = message.text

    if user_input == '/ask':
        bot.reply_to(message, "💬 Please ask your question, e.g., /ask What is the weather today?")
    else:
        user_input = user_input[len('/ask '):]

        loading_message = bot.reply_to(message, "Answer is loading...")

  # MADE BY NEP CODER(@SH0NU)
        chatgpt_url = f'https://chatgpt.apinepdev.workers.dev/?question={user_input}'
        chatgpt_response = requests.get(chatgpt_url)

        try:
            chatgpt_response.raise_for_status()
            chatgpt_data = chatgpt_response.json()
            answer = chatgpt_data.get('answer', 'I am sorry, I cannot answer your question at the moment. Please ask another question.')
            response_with_emoji = "💭 " + answer

      # MADE BY NEP CODER(@SH0NU)
            bot.edit_message_text(response_with_emoji, message.chat.id, loading_message.message_id)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            bot.edit_message_text("⚠️ An error occurred while processing your request. Please try again later.", message.chat.id, loading_message.message_id)

# MADE BY NEP CODER(@SH0NU)

@bot.message_handler(commands=['quote'])
def quote_command(message):
   # MADE BY NEP CODER(@SH0NU)
    quote_url = 'https://apinepdevs.000webhostapp.com/randomquote/'
    quote_response = requests.get(quote_url)

    try:
        quote_response.raise_for_status()
        quote_data = quote_response.json()
        quote = quote_data.get('quote', 'No quotes available at the moment.')
        author = quote_data.get('author', 'Unknown')

    # MADE BY NEP CODER(@SH0NU)
        formatted_quote = f'💡 "{quote}"\n- {author}'

        bot.reply_to(message, formatted_quote)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        bot.reply_to(message, "An error occurred while fetching a quote. Please try again later.")
        
@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    user = message.from_user
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    user_id = user.id
    is_bot = user.is_bot

    response_text = "👤 Your User Information\n\n"
    response_text += f"ℹ️ First Name: {first_name}\n"
    response_text += f"ℹ️ Last Name: {last_name}\n"
    response_text += f"🆔 Telegram ID: {user_id}\n"
    response_text += f"🆔 Username: @{username}\n"
    response_text += f"🤖 Is Bot: {is_bot}"

    bot.send_message(message.chat.id, response_text)



@bot.message_handler(commands=['short'])
def short(message):
  # MADE BY NEP CODER(@SH0NU)
    url = message.text.split(' ', 1)
    if len(url) < 2:
        bot.send_message(message.chat.id, "Please provide a valid URL. Usage: /short https://example.com")
        return

    url = url[1]

# MADE BY NEP CODER(@SH0NU)
    tinyurl_api_url = f"http://tinyurl.com/api-create.php?url={url}"
    response = requests.get(tinyurl_api_url)

    if response.status_code == 200:
        shortened_url = response.text

# MADE BY NEP CODER(@SH0NU)
        bot.send_message(message.chat.id, f"Shortened URL: {shortened_url}", disable_web_page_preview=True)

    else:
        bot.send_message(message.chat.id, "An error occurred while shortening the URL. 🔗")

@bot.message_handler(commands=['qr'])
def generate_qr_code(message):
    try:
  # MADE BY NEP CODER(@SH0NU)
        qr_text = message.text.split(' ', 1)[1]

        # MADE BY NEP CODER(@SH0NU)
        api_url = "https://qrcode.apinepdev.workers.dev/?url=" + qr_text

        # MADE BY NEP CODER(@SH0NU)
        response = requests.get(api_url)
        if response.status_code == 200:
            with open("qr_code.png", "wb") as f:
                f.write(response.content)

     
            with open("qr_code.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "Failed to generate the QR code. 🚫")
    except Exception as e:
        bot.reply_to(message, "Please use /qr followed by the text or URL to generate a QR code. 🚫")

@bot.message_handler(commands=['scrape'])
def scrape(message):
    try:
        chat_id = message.chat.id

# MADE BY NEP CODER(@SH0NU)
        if len(message.text.split()) < 2:
            bot.send_message(chat_id=chat_id, text="Please provide a website URL after the /scrape command.")
            return

# MADE BY NEP CODER(@SH0NU)
        url = message.text.split()[1]

     # MADE BY NEP CODER(@SH0NU)
        response = requests.get(url)

   # MADE BY NEP CODER(@SH0NU)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')

         # MADE BY NEP CODER(@SH0NU)
            html_text = str(soup)
            sanitized_text = html.escape(html_text)


            chunk_size = 4000  
            chunks = [sanitized_text[i:i + chunk_size] for i in range(0, len(sanitized_text), chunk_size)]

            # MADE BY NEP CODER(@SH0NU)
            for chunk in chunks:
                bot.send_message(chat_id=chat_id, text=chunk, parse_mode='HTML')
        else:
            bot.send_message(chat_id=chat_id, text="Failed to fetch the website. Status code: " + str(response.status_code))
    except Exception as e:
        bot.send_message(chat_id=chat_id, text="An error occurred: " + str(e))

@bot.message_handler(commands=['note'])
def note_command(message):
    user_input = message.text

    if user_input == '/note':
        bot.reply_to(message, "📝 Please use /note followed by the text you want to create a note image for, e.g., /note Hello, this is my note.")
    else:
        user_input = user_input[len('/note '):]

        # MADE BY NEP CODER(@SH0NU)
        note_url = f'https://notes.apinepdev.workers.dev/?text={user_input}'

      # MADE BY NEP CODER(@SH0NU)
        bot.send_photo(message.chat.id, note_url)

@bot.message_handler(commands=['meme'])
def meme_command(message):
# MADE BY NEP CODER(@SH0NU)
    meme_url = 'https://nepcoder.apinepdev.workers.dev/random-meme'
    meme_response = requests.get(meme_url)

    try:
        meme_response.raise_for_status()
        meme_data = meme_response.json()
        meme_image_url = meme_data.get('url', 'No memes available at the moment')

 
        image_response = requests.get(meme_image_url)
        image_data = image_response.content


        if len(image_data) > 20 * 1024 * 1024:  
            bot.reply_to(message, "The meme image is too large to send.")
        else:

            bot.send_photo(message.chat.id, io.BytesIO(image_data))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        bot.reply_to(message, "An error occurred while fetching memes. Please try again later.")

@bot.message_handler(commands=['image'])
def image_command(message):
    user_input = message.text

    if user_input == '/image':
        bot.reply_to(message, "🖼️ Please use /image followed by the name of the image you're looking for, e.g., /image cute cats")
    else:
        user_input = user_input[len('/image '):]
 
        pixabay_url = f'https://texttoimage.apinepdev.workers.dev/?search={user_input}'
        pixabay_response = requests.get(pixabay_url)
        pixabay_response.raise_for_status()
        pixabay_data = pixabay_response.json()

        if 'hits' in pixabay_data and len(pixabay_data['hits']) > 5:
            image_urls = [hit['largeImageURL'] for hit in pixabay_data['hits'][:5]]  # Display up to 5 results
            for image_url in image_urls:
                bot.send_photo(message.chat.id, image_url)
        else:
            bot.reply_to(message, "No images found for that query.")
            

@bot.message_handler(commands=['screenshot'])
def take_screenshot(message):

    try:
        url = message.text.split(' ', 1)[1]
        screenshot_url = f"https://screenshot.apinepdev.workers.dev/?url={url}"


        response = requests.get(screenshot_url)
        
        if response.status_code == 200:
        
            if response.headers.get('Content-Type', '').startswith('image'):
                bot.send_photo(message.chat.id, screenshot_url)
            else:
                bot.reply_to(message, "❌ The URL doesn't return a valid image. Please provide a valid web page URL.")
        else:
            bot.reply_to(message, "❌ An error occurred while taking the screenshot. Please check the URL and try again.")
    except IndexError:
        bot.reply_to(message, "Please provide a valid URL. Usage: /screenshot https://example.com")
    except Exception as e:
        bot.reply_to(message, f"❌ An error occurred: {str(e)}")





@bot.message_handler(commands=['hindijokes'])
def hindijokes_command(message):

    hindijokes_url = 'https://hindijokes.apinepdev.workers.dev/'
    hindijokes_response = requests.get(hindijokes_url)

    try:
        hindijokes_response.raise_for_status()
        hindijokes_data = hindijokes_response.json()
        joke = hindijokes_data.get('hindi_Jokes', 'No Hindi jokes available at the moment.')
        bot.reply_to(message, joke)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        bot.reply_to(message, "An error occurred while fetching Hindi jokes. Please try again later.")

@bot.message_handler(commands=['photo'])
def photo_command(message):
    bot.reply_to(message, "📷 Please send a photo to convert it to an image URL.")

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        photo = message.photo[-1]

        file_info = bot.get_file(photo.file_id)
        image_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

        image_response = requests.get(image_url)
        image_data = image_response.content

        image_file = io.BytesIO(image_data)

        formData = {'file': ('image.jpg', image_file)}

        telegraph_response = requests.post('https://telegra.ph/upload', files=formData)

        photo_url = telegraph_response.json()[0]['src']

        bot.send_message(message.chat.id, f'🔗 Image URL: https://telegra.ph{photo_url}')
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Error: {e}')


@bot.message_handler(commands=['weather'])
def get_weather(message):

    try:
        city_name = message.text.split(' ', 1)[1]
        weather_url = f"https://weather.apinepdev.workers.dev/?cityname={city_name}"
        response = requests.get(weather_url)

        if response.status_code == 200:
            weather_data = response.json()
            current = weather_data.get('current', {})


            temperature = current.get('temp_c')
            condition = current.get('condition', {}).get('text')
            humidity = current.get('humidity')
            wind_speed = current.get('wind_kph')
            
            # Emojis
            sun_emoji = "☀️"
            cloud_emoji = "⛅"
            humidity_emoji = "💧"
            wind_emoji = "🌬️"

     
            response_text = f"{sun_emoji} Weather in {city_name} {sun_emoji}:\n"
            response_text += f"Temperature: {temperature}°C\n"
            response_text += f"Condition: {cloud_emoji} {condition}\n"
            response_text += f"Humidity: {humidity_emoji} {humidity}%\n"
            response_text += f"Wind Speed: {wind_emoji} {wind_speed} km/h"

    
            bot.reply_to(message, response_text)
        else:
            bot.reply_to(message, "❌ Sorry, I couldn't fetch weather information for that city. Please check the city name.")
    except IndexError:
        bot.reply_to(message, "🌍 Please provide a valid city name. Usage: /weather cityname")
        

@bot.message_handler(commands=['encode'])
def encode_text(message):
    user_input = message.text[len('/encode '):].strip()
    
    if user_input:
        response = requests.get(encode_api_url + user_input)
        data = json.loads(response.text)

        if data.get('status') == 'success':
            encoded_data = data.get('encodedForm', '')
            bot.reply_to(message, f'🔒 Encoded Text: {encoded_data}')
        else:
            bot.reply_to(message, 'Failed to encode the provided text. Make sure it is valid text data.')
    else:
        bot.reply_to(message, 'Please provide text to encode. Usage: /encode your_text_here')

@bot.message_handler(commands=['decode'])
def decode_text(message):
    user_input = message.text[len('/decode '):].strip()

    if user_input:
        response = requests.get(decode_api_url + user_input)
        data = json.loads(response.text)

        if data.get('status') == 'success':
            decoded_data = data.get('decodedForm', '')
            bot.reply_to(message, f'🔓 Decoded Text: {decoded_data}')
        else:
            bot.reply_to(message, 'Failed to decode the provided text. Make sure it is valid base64 encoded data.')
    else:
        bot.reply_to(message, 'Please provide base64 encoded text to decode. Usage: /decode your_encoded_text_here')




        
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    if not user_input.startswith(('/', '💬 Please use')):
        bot.reply_to(message, "I don't understand that. Type /help for a list of available commands.")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=10)



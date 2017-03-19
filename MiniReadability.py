import urllib.request
from bs4 import BeautifulSoup


class MiniReadability(object):

    __url = ""
    __name_of_file = ""
    __text = ""

    def text(self):
        return self.__text

    def url(self):
        return self.__url

    def name_of_file(self):
        return self.__name_of_file

    def __init__(self, url):

        self.__url = url
        self.__import_site()
        self.__create_new_text_file()

    # input method use urllib
    def __import_site(self):

        site = b''
        try:
            site = urllib.request.urlopen(self.__url).read()
        except:
            print('That is unreadable URL')
            exit(0)

        try:
            self.__text = site.decode()
        # Some sites don't decoding with utf-8
        except:
            try:
                self.__text = site.decode("cp1251")
            # If something is wrong
            except:
                print('It is untranslated site code')
                exit(0)

    # All working with text file
    def __create_new_text_file(self):
        # Translating URL to normal form for text file
        self.__create_beautiful_filename()
        # Working with text
        self.__create_text()
        self.__make_text_beautiful()

        # Entering text into the new file
        new_file = open(self.__name_of_file, mode="w", encoding='utf-8')
        new_file.write(self.__text)
        new_file.close()

    # Work with content of text.
    def __create_text(self):

        if self.__text.find('<article') != -1:
            self.__text = self.__text[self.__text.find('<article'): self.__text.rfind('</article>')]

        # Deleting impostors
        impostors = ["<li><", "<li>\n", "<li ", "<p><"] # , "</ul></li>"]
        for imp in impostors:
            self.__text = self.__text.replace(imp, '')

        # Taking all inside only <p>...</p> and <li>...</li>
        full_text = self.__text
        self.__text = ""

        header = "    " + self.search_text_between(full_text, "<h1", "</h1>", mode=1) + "\n\n"

        tags = [["<h2>", "<h3>", "<p>", "<li>", "<dd>"], ["</h2>", "</h3>", "</p>", "</li>", "</dd>"]]

        # Running on tags and checking them
        while len(tags[0]) != 0:
            run_away = False
            min = len(full_text)

            for tag in tags[0]:
                index = tags[0].index(tag)
                place_of_tag = full_text.find(tag)

                if place_of_tag == -1:
                    tags[0].pop(index)
                    tags[1].pop(index)
                    run_away = True
                    break
                else:
                    if place_of_tag < min:
                        min = place_of_tag
                        min_index = index

            # if all right, pasting fragment
            if len(tags[0]) != 0 and run_away is False:
                to_paste = self.search_text_between(full_text, tags[0][min_index], tags[1][min_index])
                if to_paste != "":
                    if tags[0][min_index] == "<li>":
                        self.__text += "· " + to_paste + "\n"
                    if tags[0][min_index] == "<p>" or tags[0][min_index] == "<dd>":
                        self.__text += to_paste + "\n"
                    if tags[0][min_index] == "<h2>" or tags[0][min_index] == "<h3>":
                        # h2, h3 have "    " before text
                        self.__text += "    " + to_paste + "\n"
                full_text = full_text[min + 1:]

        if self.__text == "":
            print("This site has not right text content")
            exit(0)

        self.__text = header + self.text()

    # Working with text format.
    def __make_text_beautiful(self):

        # Working with links. Translating that to [...] format.
        while self.__text.find('<a') != -1:
            self.__mega_replace('<a', '</a>', '>', '<', 'url')

        self.__text = self.__text.replace("[]", "[inside link]")

        # Deleting unnecessary empty lines.
        while self.__text.find("\n\n") != -1:
            self.__text = self.__text.replace("\n\n", "\n")

        soup = BeautifulSoup(self.__text, "html.parser")
        self.__text = soup.get_text()

        # It is changing BAD-HTML-space to normal space
        self.__text = self.__text.replace(" ", " ")

# ------------------------------------------------------------# Making strings length = 80 symbols
        text_list = list(self.__text)
        self.__text = ""

        count = 0
        # Points of separation, if it is need
        last_space = 0
        # Counter. Is need separation or not
        symbols_count = 0

        for sym in text_list:
            count += 1
            symbols_count += 1
            if sym == " ":
                last_space = count-1
            # This is old '\n'. That is just making indent between paragraphs.
            if sym == "\n":
                text_list[count - 1] += '\n'
                symbols_count = 0
                last_space = 0
            # This is new '\n'. Needed new line for long string.
            if symbols_count >= 80:
                # No last space. Needed word separation.
                if last_space == 0:
                    text_list[count - 1] += '\n'
                    symbols_count = 0
                    last_space = 0
                # It is last space in new line
                else:
                    text_list[last_space] += '\n'
                    symbols_count = count - last_space
                    last_space = 0

# ------------------------------------------------- Returning back to __text new 80-length-strings
        for sym in text_list:
            self.__text += sym

    # Working with url and creating correct name for new file
    def __create_beautiful_filename(self):

        self.__name_of_file = self.__url

        if self.__name_of_file.find('/') != -1:
            self.__name_of_file = self.__name_of_file[self.__name_of_file.find("/"):]
        self.__name_of_file = self.__name_of_file[:self.__name_of_file.find(".html")]

        self.__name_of_file = r"[CUR_DIR]" + self.__name_of_file + ".txt"

        # All unaccess symbols are replacing to "_"
        symbols = ['/', '\\', '|', '"', ':', '>', '<', '*', '?']
        for sym in symbols:
            self.__name_of_file = self.__name_of_file.replace(sym, '_')

    # Replacing fragment to fragment, that is in the first fragment.
    def __mega_replace(self, marker_before, marker_after, marker_before_inside, marker_after_inside, mode=""):

        fragment_to_replacement = self.search_text_between(self.__text, marker_before, marker_after, 3)
        new_fragment = self.search_text_between(fragment_to_replacement, marker_before_inside, marker_after_inside)
        url_fragment = self.search_text_between(fragment_to_replacement, "=", " ")[1:-1]

        if url_fragment[0:4] != "http":
            url_fragment = ""
        if mode == "":
            self.__text = self.__text.replace(fragment_to_replacement, new_fragment)
        if mode == "url":
            self.__text = self.__text.replace(fragment_to_replacement, new_fragment + ' [' + url_fragment + ']')

    # This method return fragment between two markers. (mode = 0) => without markers. Else => with them.
    @staticmethod
    def search_text_between(text, marker_before, marker_after, mode=0):
        if text.find(marker_before) == -1 or text.find(marker_after) == -1:
            return ""
        start_of_text = text.find(marker_before)
        end_of_text = text.find(marker_after, start_of_text)
        if mode == 0:
            start_of_text += len(marker_before)
        else:
            end_of_text += len(marker_after)
        text = text[start_of_text:end_of_text]
        return text

import urllib.request
from html.parser import HTMLParser


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

    # TODO
    # input method use urllib
    def __import_site(self):

        site = b''
        try:
            site = urllib.request.urlopen(self.__url).read()
        except:
            print('ERROR!!! Unreadable URL')
            exit(0)

        try:
            self.__text = site.decode()

        except:
            self.__text = site.decode("cp1251")
        #    print('ERROR!!! Problem with site decoding')
        #    exit(0)

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

    # Work with content of text. TODO
    def __create_text(self):

        while self.__text.find("<p ") != -1:
            to_delete = self.search_text_between(self.__text, "<p ", "</p>", mode=1)
            self.__text = self.__text.replace(to_delete, "")

        while self.__text.find("<li ") != -1:
            to_delete = self.search_text_between(self.__text, "<li ", "</li>", mode=1)
            self.__text = self.__text.replace(to_delete, "")

        while self.__text.find("<li><a") != -1:
            to_delete = self.search_text_between(self.__text, "<li><a", "</li>", mode=1)
            self.__text = self.__text.replace(to_delete, "")
        self.__text = self.__text.replace("</ul></li>", "")

        # self.__text = self.__text[self.__text.find('<body'): self.__text.find('</body>')]
        # self.__text = self.__text[self.__text.find('</header>') + len('</header>'): self.__text.find('<footer')]
        # self.__text = self.__text[self.__text.find('<p>'): self.__text.find('<div id="content-bottom">')]

        self.__text = self.__text.replace('<p>', "@@@")
        self.__text = self.__text.replace('<li>', "@@@· ")
        tags = ['</p>', '</li>']
        for tag in tags:
            self.__text = self.__text.replace(tag, "$$$%%%")

        if self.__text == "":
            print("This site has not text content")
            exit(0)

        self.__text = self.__text[self.__text.find("@@@"): self.__text.rfind("%%%")]
        self.__text = "%%%" + self.__text
        #print(self.__text)
        while self.__text.find('@@@') != -1:
            self.__mega_replace('%%%', '$$$', '@@@', '$$$')




    # Working with format of text. TODO
    def __make_text_beautiful(self):

        while self.__text.find('<a') != -1:
            self.__mega_replace('<a', '</a>', '=', ' target', 'url')

        while self.__text.find('<span') != -1:
            self.__mega_replace('<span', 'span>', '>', '</')#, "without \n")

        symbols = ['<b>', '</b>', '<i>', '</i>', '<small>', '</small>', '<br>', '<br />']
        for sym in symbols:
            self.__text = self.__text.replace(sym, '')

        self.__text = self.__text.replace("[]", "")
        while self.__text.find("\n\n") != -1:
            self.__text = self.__text.replace("\n\n", "\n")
        self.__text = self.__text.replace(" ", " ")  # It is changing BAD-HTML-space to normal space

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
        if mode == "":
            self.__text = self.__text.replace(fragment_to_replacement, new_fragment + "\n")
        if mode != "" and mode != "url":
            self.__text = self.__text.replace(fragment_to_replacement, new_fragment)
        if mode == "url":
            self.__text = self.__text.replace(fragment_to_replacement, '[' + new_fragment + ']')

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

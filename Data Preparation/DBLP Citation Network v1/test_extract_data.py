from extract_data import Author, Paper, Venue, parse_title, parse_authors, parse_year, parse_venue, parse_abstract, parse_reference, parse_id, parse_paper, extract_data
from unittest.mock import patch, mock_open

def test_parse_title():
    # parse_title takes 2 arguments, start and lines
    # start is the index of the line where the title starts
    # lines is a list of lines of the file
    # it returns the title of the paper


    assert parse_title(0, ["This is a test title","\n"]) == "This is a test title"
    assert parse_title(0, ["This is a test title", "and this is its continuation","\n"]) == "This is a test title and this is its continuation"
    assert parse_title(1, ["This is a test title", "#*and this is its continuation","\n"]) == "and this is its continuation"
    assert parse_title(0, ["This is a test title", "#*This is a new test title"]) == "This is a test title"
    assert parse_title(0, ["#*This is a test title", "#*This is a new test title", "#*"]) == "This is a test title"

def test_parse_authors():
    # parse_authors takes 2 arguments, start and lines
    # start is the index of the line where the authors start
    # lines is a list of lines of the file
    # it returns a list of authors of the paper

    assert parse_authors(0, ["This is a test author","\n"])[0].name == [Author("This is a test author")][0].name

    authors = parse_authors(0, ["This is a test author, This is another test author","\n"])
    assert authors[0].name == "This is a test author"
    assert authors[1].name == "This is another test author"

    authors = parse_authors(0, ["This is the fir", "st author, This is the second author","\n"])
    assert authors[0].name == "This is the first author"
    assert authors[1].name == "This is the second author"

    authors = parse_authors(0, ["#@First Author, Second Author", ",Third Author, Fourth Auth", "or, Fifth Author", "#Author of another paper","\n"])
    assert authors[0].name == "First Author"
    assert authors[1].name == "Second Author"
    assert authors[2].name == "Third Author"
    assert authors[3].name == "Fourth Author"
    assert authors[4].name == "Fifth Author"

    authors = parse_authors(0, ["#@First Author,", "Second Author", ",Third Author, Fourth Auth", "or, Fifth Author", "#@Author of another paper","\n"])
    assert authors[0].name == "First Author"
    assert authors[1].name == "Second Author"
    assert authors[2].name == "Third Author"
    assert authors[3].name == "Fourth Author"
    assert authors[4].name == "Fifth Author"

    authors = parse_authors(3, ["#@First Author, Second Author", "Third Author, Fourth Auth", "or, Fifth Author", "#@Author of another paper","\n"])
    assert authors[0].name == "Author of another paper"

def test_parse_year():
    # parse_year takes 2 arguments, start and lines
    # start is the index of the line where the year starts
    # lines is a list of lines of the file
    # it returns the year of the paper

    assert parse_year(0,["#t2019","\n"]) == 2019
    assert parse_year(0,["#t2019"]) == 2019
    assert parse_year(1,["#t2019", "#t2020","\n"]) == 2020
    assert parse_year(0,["#t2019", "#t2020", "#t2021"]) == 2019
    assert parse_year(2,["#t2019", "#t2020", "#t2021"]) == 2021

def test_parse_venue():
    # parse_venue takes 2 arguments, start and lines
    # start is the index of the line where the venue starts
    # lines is a list of lines of the file
    # it returns the venue of the paper

    assert parse_venue(0,["#cVenue","\n"]).name == "Venue"
    assert parse_venue(0,["#cVenue","#something"]).name == "Venue"
    assert parse_venue(1,["#cVenue", "#cNew Venue","\n"]).name == "New Venue"
    assert parse_venue(0,["#cThis", " is the venue","\n"]).name == "This is the venue"
    assert parse_venue(0,["#cThis", " is", " the", " venue","\n"]).name == "This is the venue"

def test_parse_abstract():
    # parse_abstract takes 2 arguments, start and lines
    # start is the index of the line where the abstract starts
    # lines is a list of lines of the file
    # it returns the abstract of the paper

    assert parse_abstract(0,["#!This is the abstract","\n"]) == "This is the abstract"
    assert parse_abstract(0,["#!This is the abstract", "and this is its continuation","\n"]) == "This is the abstract and this is its continuation"
    assert parse_abstract(1,["#!This is the abstract", "#!This is a new abstract","#something"]) == "This is a new abstract"
    assert parse_abstract(0,["#!This is the abstract", "#!This is a new abstract"]) == "This is the abstract"
    assert parse_abstract(0,["#!This is the abstract", "#!This is a new abstract", "#!"]) == "This is the abstract"

def test_parse_reference():
    # parse_reference takes 2 arguments, start and lines
    # start is the index of the line where the reference starts
    # lines is a list of lines of the file
    # it returns a reference of the paper

    assert parse_reference(0,["#%436405","\n"]).id == "436405"
    assert parse_reference(0,["#%436405","#something"]).id == "436405"
    assert parse_reference(0,["#%436406"]).id == "436406"
    assert parse_reference(1,["#%436405", "#%436406","\n"]).id == "436406"

def test_parse_id():
    # parse_id takes 2 arguments, start and lines
    # start is the index of the line where the id starts
    # lines is a list of lines of the file
    # it returns the id of the paper

    assert parse_id(0,["#index436405","\n"]) == "436405"
    assert parse_id(0,["#index436405","#something"]) == "436405"
    assert parse_id(0,["#index436406"]) == "436406"
    assert parse_id(1,["#index436405", "#index436406","\n"]) == "436406"

def test_parse_paper():
    # parse_paper takes 2 arguments, start and lines
    # start is the index of the line where the paper starts
    # lines is a list of lines of the file
    # it returns a dictionary with the id, title, authors, year, venue, abstract and references of the paper

    paper = parse_paper(0, ["#index436405", "#*This is a test title", "#@This is a test author", "#t2019", "#cVenue", "#!This is the abstract", "#%436406","\n"])
    assert paper["id"] == "436405"
    assert paper["title"] == "This is a test title"
    assert paper["authors"][0].name == "This is a test author"
    assert paper["year"] == 2019
    assert paper["venue"].name == "Venue"
    assert paper["abstract"] == "This is the abstract"
    assert paper["references"][0].id == "436406"

def test_extract_data():
    # extract_data takes 1 argument, filename
    # filename is the name of the file to be parsed
    # it returns a list of papers in the file

    with patch('extract_data.Paper.insert') as mock_insert, \
         patch('extract_data.Paper.add_author') as mock_add_author, \
         patch('extract_data.Paper.add_venue') as mock_add_venue, \
         patch('extract_data.Paper.add_reference') as mock_add_reference, \
         patch('extract_data.Author.insert') as mock_insert, \
         patch('extract_data.Venue.insert') as mock_insert, \
         patch('extract_data.parse_paper') as mock_parse_paper:

        # Configure mock methods to do nothing
        mock_insert.return_value = None
        mock_add_author.return_value = None
        mock_add_venue.return_value = None
        mock_add_reference.return_value = None
        mock_parse_paper.return_value = {"id": "436405", "title": "This is a test title", "authors": [Author("This is a test author")], "year": 2019, "venue": Venue("Venue"), "abstract": "This is the abstract", "references": [Paper("436406")]}


        sample_lines = [" ","#*This is a test title, #index436405", "#@This is a test author", "#t2019", "#cVenue", "#!This is the abstract", "#%436406","\n"]
        # Mock the open function
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            # Customize the file-like object's readlines behavior
            mock_file.return_value.readlines.return_value = sample_lines

            extract_data()
        mock_insert.assert_called_once()
        mock_add_author.assert_called_once()
        mock_add_venue.assert_called_once()
        mock_add_reference.assert_called_once()
        mock_parse_paper.assert_called_once()
        mock_parse_paper.assert_called_once_with(1, sample_lines)



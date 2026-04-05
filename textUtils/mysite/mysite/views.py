# i have created this file

from django.http import HttpResponse
from django.shortcuts import render



def index2(request):
    return render(request, 'index.html')

def analyzer(request):
    # get the text
    text = request.POST.get('text', 'default')
    removepunch = request.POST.get('removepunch', 'off')
    iscapital = request.POST.get('fullcapitalize','off')
    newlineremover = request.POST.get('newlineremover','off')
    extraspaceremover = request.POST.get('extraspaceremover','off')
    charcount = request.POST.get('charcount', 'off')

    # Start with original text
    analyzed = text
    purpose_list = []
  
    # Apply transformations in sequence (allows multiple tasks to work together)
    if removepunch == 'on':
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        temp = ""
        for i in analyzed:
            if i not in punctuations:
                temp += i
        analyzed = temp
        purpose_list.append('Remove Punctuation')

    if iscapital == 'on':
        analyzed = analyzed.upper()
        purpose_list.append('Capitalize')
    
    if newlineremover == 'on':
        analyzed_temp = ""
        for char in analyzed:
            if char != '\n' and char != '\r':
                analyzed_temp += char
        analyzed = analyzed_temp
        purpose_list.append('Remove New Lines')

    if extraspaceremover == 'on':
        analyzed_temp = ""
        for index, char in enumerate(analyzed):
            if not (char == " " and index + 1 < len(analyzed) and analyzed[index + 1] == " "):
                analyzed_temp += char
        analyzed = analyzed_temp
        purpose_list.append('Remove Extra Spaces')
    

    # Add character count info if selected
    if charcount == 'on':
        char_count = len(analyzed)
        analyzed = f"{analyzed}\n\n--- Character Count: {char_count} ---"
        purpose_list.append('Character Count')


    # If no operations were selected, return error
    if not purpose_list:
        return HttpResponse("ERROR")

    
    # Combine all purposes
    purpose = ' + '.join(purpose_list)
    params = {'purpose': purpose,
              'analyzed_text': analyzed}
    
    return render(request, 'analyzer.html', params)
    
    # analyize the text and capitalize it wants
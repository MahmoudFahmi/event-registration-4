contacts_list = [
        ('Alice Brown', False, '1231112223'),
        ('Bob Crown', 'bob@crowns.com', False),
        ('Carlos Drew', 'carl@drewess.com',3453334445),
        ('Doug Emerty', False,'4564445556'),
        ('Egan Fair', 'eg@fairness.com', 5675556667)
    ]

leads_list = [
    (False, 'kevin@keith.com',False),
    ('Lucy', 'lucy@liu.com', '3210001112'),
    ('Mary Middle', 'mary@middle.com', '3331112223'),
    (False, False, '4442223334'),
    (False, 'ole@olson.com', False),
]

registrants = [
               ('Lucy Liu', 'lucy@liu.com', 2547894560),
               ('Doug', 'doug@emmy.com', 4564445556),
               ('Uma Thurman', 'uma@thurs.com', False)]

import re,json
class Contact:

    def __init__(self, client_name, email=False, phone=False):
        self.client_name = client_name
        self.email = email
        self.phone = phone

    @property
    def client_name(self):
        return self._client_name

    @client_name.setter
    def client_name(self, n):
        if not n:
            raise Exception("Name cannot be empty")
        self._client_name = n


class Lead:

    def __init__(self, lead_name, email, phone):
        self.lead_name = lead_name
        self.email = email
        self.phone = phone


def register(registration_data):
    data = json.loads(registration_data)
    if data['registrant'].get('phone') and not re.match(r'(^\d{10}$)', str(data['registrant'].get('phone'))):
        raise Exception("Invalid Phone Number")
    contact_found = False
    for contact in contacts_list:
        # match registrant's email to Contacts list
        if data['registrant'].get('email') and contact[1] == data['registrant'].get('email'):
            contact_found = True
            # if registrant mail matched contact mail and registrant data include phone other than contact's phone
            # and contact's phone is not empty
            # we update the contact phone with the new one
            if contact[2] and contact[2] != data['registrant'].get('phone'):
                contact = list(contact)
                contact[2] = data['registrant'].get('phone')
                contact = tuple(contact)
        # match registrant's phone to Contacts list
        elif data['registrant'].get('phone') and contact[2] == data['registrant'].get('phone'):
            contact_found = True
            # if registrant's phone matched contact's phone and registrant data include mail other than contact's mail
            # and contact's mail is not empty
            # we update the contact's mail with the new one
            if contact[1] and contact[1] != data['registrant'].get('mail'):
                contact = list(contact)
                contact[2] = data['registrant'].get('mail')
                contact = tuple(contact)
        if contact_found:
            break
    # if registrant's data (mail or phone) does not match any contacts list data
    # try to match it wit leads list data

    if not contact_found:
        lead_found = False
        for lead in leads_list:
            if data['registrant'].get('email') and lead[1] == data['registrant'].get('email') or \
                        data['registrant'].get('phone') and contact[1] == data['registrant'].get('phone'):
                # if lead's data (email , or phone ) matched with registrant's data ==>
                # create new contact with the new data and remove the lead from Leads List
                new_contact = (data['registrant'].get('name'), data['registrant'].get('mail'), data['registrant'].get('phone'))
                contacts_list.append(new_contact)
                leads_list.remove(lead)
                lead_found = True
                break
    # if registrant's data does not matched with any contact's data or lead's data ==>
    # create a new Contact
    if not contact_found and not lead_found:
        new_contact = (data['registrant'].get('name'), data['registrant'].get('mail'), data['registrant'].get('phone'))
        contacts_list.append(new_contact)

for registrant in registrants:
    registration_data = json.dumps({
          "registrant":
             {
                "name": registrant[0],
                "email": registrant[1],
                "phone": registrant[2],
             }
        })
    register(registration_data)


from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile, CoursesOffered, TutorProfile, StudentProfile, ClassRequest
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login



CITY_CHOICES = (('Sylhet', 'Sylhet',), ('Dhaka', 'Dhaka',), ('Khulna', 'Khulna',), ('Rajshahi', 'Rajshahi',))
LEVEL_CHOICES = (('Primary', 'Primary',), ('Secondary', 'Secondary',), ('High School', 'High School',))

PRIMARY_CHOICES = (('Mathematics','Mathematics'), ('English','English'), ('Bangla','Bangla'), ('Science','Science'),)
SECONDARY_CHOICES = (('Mathematics','Mathematics'), ('Physics','Physics'),  ('Chemistry','Chemistry'), ('Biology','Biology'),
                    ('Social','Social'), ('English', 'English'), ('Bangla','Bangla'))
HIGH_CHOICES = (('Mathematics','Mathematics'), ('Physics','Physics'),  ('Chemistry','Chemistry'), ('Biology','Biology'),
                ('Social Sciences','Social Sciences'), ('ICT','ICT'), ('English', 'English'), ('Bangla','Bangla'))


class ClassRequestForm(forms.ModelForm):
    class Meta:
        model = ClassRequest
        fields = ('msg',)

    msg = forms.CharField(max_length=1500,
    widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
            'rows':'5'
        }
    ))


class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('school', 'grade', 'fav_subjects', 'description', 'student_image')

    school = forms.CharField(max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
        }
    ))
    fav_subjects = forms.CharField(max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
        }
    ))
    student_image = forms.ImageField()
    description = forms.CharField(max_length=1500,
    widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
            'rows':'5'
        }
    ))
    grade = forms.IntegerField(widget=forms.NumberInput(
    attrs={
        'class': 'form-control',
        'autocomplete':'off',
    }
    ))



class EditTutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ('edu_qualification', 'expertise', 'tutor_image', 'description', 'charge_hr')

    edu_qualification = forms.CharField(max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
        }
    ))
    expertise = forms.CharField(max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
        }
    ))
    tutor_image = forms.ImageField()
    description = forms.CharField(max_length=1500,
    widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'autocomplete':'off',
            'rows':'5'
        }
    ))
    charge_hr = forms.IntegerField(widget=forms.NumberInput(
    attrs={
        'class': 'form-control',
        'autocomplete':'off',
    }
    ))


class CourseSelectionForm(forms.ModelForm):
    class Meta:
        model = CoursesOffered
        fields = ('city', 'study_level', 'subject',)

class CourseSearchForm(forms.Form):
    study_level = forms.ChoiceField(choices = LEVEL_CHOICES,
    widget = forms.Select(
        attrs={
            'class': 'form-control',
            'id': 'levelChoice',
        }
    ))


class TutorSearchForm(forms.Form):
    study_level = forms.ChoiceField(choices = LEVEL_CHOICES,
    widget = forms.Select(
        attrs={
            'class': 'form-control',
            'id': 'levelChoice',
        }
    ))

class UserInfoForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name',
            'autocomplete':'off',
        }
    ))
    profession = forms.CharField(max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Profession',
            'autocomplete':'off',
        }
    ))
    city = forms.ChoiceField(choices = CITY_CHOICES,
    widget = forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))
    CHOICES_TYPE = (('Student', 'Student',), ('Tutor', 'Tutor',))
    user_type = forms.ChoiceField(choices = CHOICES_TYPE,
    widget = forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))
    class Meta:
        model = UserProfile
        fields = ('full_name', 'profession', 'city', 'user_type',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(min_length=4, max_length=150,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete':'off',
        }
    ))
    password = forms.CharField(
    widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete':'off',
        }
    ))


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
        }
    ))
    username = forms.CharField(min_length=7, max_length=12,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }
    ))
    password1 = forms.CharField(
    widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))
    password2 = forms.CharField(
    widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Retype password',
        }
    ))
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user

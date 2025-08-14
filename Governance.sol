pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//evault solidity code
contract Governance {

    uint public hospitalCount = 0; 
    mapping(uint => hospital) public hospitalList; 
     struct hospital
     {
       string hospital_details;
     }
 
   // events 
   event hospitalCreated(uint indexed _hospitalId);
   
   //function  to save hospital details to Blockchain
   function saveHospital(string memory hd) public {
      hospitalList[hospitalCount] = hospital(hd);
      emit hospitalCreated(hospitalCount);
      hospitalCount++;
    }

     //get hospital count
    function getHospitalCount()  public view returns (uint) {
          return  hospitalCount;
    }

     function getHospital(uint i) public view returns (string memory) {
        hospital memory hl = hospitalList[i];
	return hl.hospital_details;
    }

    uint public educationCount = 0; 
    mapping(uint => education) public educationList; 
     struct education
     {
       string education_details;       
     }
 
   // events 
   event educationCreated(uint indexed _educationId);
   
   //function  to save education details to Blockchain
   function saveEducation(string memory ed) public {
      educationList[educationCount] = education(ed);
      emit educationCreated(educationCount);
      educationCount++;
    }

    //get education count
    function getEducationCount()  public view returns (uint) {
          return  educationCount;
    }

    function getEducation(uint i) public view returns (string memory) {
        education memory el = educationList[i];
	return el.education_details;
    }

    uint public studentCount = 0; 
    mapping(uint => student) public studentList; 
     struct student
     {
       string student_details;       
     }
 
   // events 
   event studentCreated(uint indexed _studentId);
   
   //function  to save student details to Blockchain
   function saveStudent(string memory sd) public {
      studentList[studentCount] = student(sd);
      emit studentCreated(studentCount);
     studentCount++;
    }

     //get student count
    function getStudentCount()  public view returns (uint) {
          return studentCount;
    }


    function getStudent(uint i) public view returns (string memory) {
        student memory sl = studentList[i];
	return sl.student_details;
    }

    uint public patientCount = 0; 
    mapping(uint => patient) public patientList; 
     struct patient
     {
       string patient_details;       
     }
 
   // events 
   event patientCreated(uint indexed _patientId);
   
   //function  to save patient details to Blockchain
   function savePatient(string memory pd) public {
      patientList[patientCount] = patient(pd);
      emit patientCreated(patientCount);
     patientCount++;
    }

     //get patient count
    function getPatientCount()  public view returns (uint) {
          return patientCount;
    }


    function getPatient(uint i) public view returns (string memory) {
        patient memory pl = patientList[i];
	return pl.patient_details;
    }

}